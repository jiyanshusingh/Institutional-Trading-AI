from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

_log = logging.getLogger("trade_scorer")

NUMERIC_FEATURES = [
    "rsi_14",
    "atr_pct",
    "volume_ratio",
    "bb_width",
    "recent_high_dist_pct",
    "recent_low_dist_pct",
    "ema20_dist_pct",
    "ema50_dist_pct",
]

CATEGORICAL_FEATURES = [
    "day_type",
    "stock_type",
    "strategy",
    "direction",
    "timeframe",
]


class TradeScorer:
    """XGBoost model that predicts P(WIN) for a trade candidate."""

    def __init__(self):
        self.model: xgb.XGBClassifier | None = None
        self.label_encoders: dict[str, LabelEncoder] = {}
        self.feature_names: list[str] = []
        self._is_fitted = False

    # ── Feature engineering ─────────────────────────────────────

    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        rows = []
        for _, row in df.iterrows():
            feat = {}
            for col in NUMERIC_FEATURES:
                val = row.get(col)
                try:
                    feat[col] = float(val) if val not in (None, "", "None") else 0.0
                except (ValueError, TypeError):
                    feat[col] = 0.0
            for col in CATEGORICAL_FEATURES:
                feat[col] = str(row.get(col, "UNKNOWN"))
            rows.append(feat)
        return pd.DataFrame(rows)

    def _encode_categoricals(self, X: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        X = X.copy()
        for col in CATEGORICAL_FEATURES:
            if col not in X.columns:
                continue
            if fit:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                self.label_encoders[col] = le
            else:
                le = self.label_encoders.get(col)
                if le is not None:
                    X[col] = (
                        X[col]
                        .astype(str)
                        .map(
                            lambda v: (
                                le.transform([v])[0] if v in le.classes_ else -1
                            )
                        )
                    )
                else:
                    X[col] = 0
        return X

    # ── Training ────────────────────────────────────────────────

    def train(
        self, csv_path: str | Path, test_size: float = 0.2, **xgb_params
    ) -> dict:
        df = pd.read_csv(csv_path)
        df = df[df["result"].isin(["WIN", "LOSS"])].copy()
        if len(df) < 50:
            raise ValueError(f"Need at least 50 resolved trades, got {len(df)}")

        df["win"] = (df["result"] == "WIN").astype(int)

        X_raw = self._prepare_features(df)
        y = df["win"].values

        X = self._encode_categoricals(X_raw, fit=True)
        self.feature_names = list(X.columns)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        params = {
            "n_estimators": 200,
            "max_depth": 5,
            "learning_rate": 0.05,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "eval_metric": "logloss",
            "random_state": 42,
        }
        params.update(xgb_params)

        self.model = xgb.XGBClassifier(**params)
        self.model.fit(
            X_train,
            y_train,
            eval_set=[(X_test, y_test)],
            verbose=False,
        )

        y_prob = self.model.predict_proba(X_test)[:, 1]
        y_pred = (y_prob >= 0.5).astype(int)
        acc = (y_pred == y_test).mean()
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        self._is_fitted = True

        return {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
        }

    # ── Inference ───────────────────────────────────────────────

    def predict_proba(self, features: dict) -> float:
        """Return P(WIN) ∈ [0, 1] for a single trade candidate."""
        if self.model is None:
            raise RuntimeError("Model not trained or loaded")

        row = {}
        for col in NUMERIC_FEATURES:
            val = features.get(col)
            try:
                row[col] = float(val) if val not in (None, "", "None") else 0.0
            except (ValueError, TypeError):
                row[col] = 0.0
        for col in CATEGORICAL_FEATURES:
            row[col] = str(features.get(col, "UNKNOWN"))

        X = pd.DataFrame([row])
        X = self._encode_categoricals(X, fit=False)
        prob = self.model.predict_proba(X)[0, 1]
        return float(prob)

    # ── Persistence ─────────────────────────────────────────────

    def save(self, path: str | Path) -> None:
        if self.model is None:
            raise RuntimeError("No model to save")
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        model_path = path.with_suffix(".json")
        self.model.save_model(str(model_path))

        encoders_data = {
            name: le.classes_.tolist()
            for name, le in self.label_encoders.items()
        }

        meta = {
            "feature_names": self.feature_names,
            "label_encoders": encoders_data,
            "numeric_features": NUMERIC_FEATURES,
            "categorical_features": CATEGORICAL_FEATURES,
        }
        meta_path = path.with_suffix(".meta.json")
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)

        _log.info(f"Model saved to {model_path}")
        _log.info(f"Metadata saved to {meta_path}")

    @classmethod
    def load(cls, path: str | Path) -> "TradeScorer":
        path = Path(path)
        model_path = path.with_suffix(".json")
        meta_path = path.with_suffix(".meta.json")

        if not model_path.exists() or not meta_path.exists():
            raise FileNotFoundError(f"Model files not found at {path}")

        scorer = cls()
        scorer.model = xgb.XGBClassifier()
        scorer.model.load_model(str(model_path))

        with open(meta_path) as f:
            meta = json.load(f)

        scorer.feature_names = meta["feature_names"]
        for name, classes in meta["label_encoders"].items():
            le = LabelEncoder()
            le.classes_ = np.array(classes)
            scorer.label_encoders[name] = le

        scorer._is_fitted = True
        return scorer
