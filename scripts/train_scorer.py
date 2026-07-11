"""
Train XGBoost trade scorer from exported backtest trade CSVs.

Usage:
    cd /Users/jiyanshusingh/Institutional-Trading-AI
    .venv/bin/python scripts/train_scorer.py --input "data/trades_*.csv"
    .venv/bin/python scripts/train_scorer.py --input "data/trades_*.csv" --output models/scorer_v1
"""

from __future__ import annotations

import argparse
import logging
import sys
from glob import glob

import pandas as pd

sys.path.insert(0, ".")
from models.trade_scorer import TradeScorer

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s %(message)s"
)
_log = logging.getLogger("train_scorer")


def main():
    parser = argparse.ArgumentParser(description="Train XGBoost trade scorer")
    parser.add_argument(
        "--input",
        required=True,
        help='Glob pattern for trade CSV files, e.g. "data/trades_*.csv"',
    )
    parser.add_argument(
        "--output",
        default="models/scorer_v1",
        help="Output model path (without extension, default: models/scorer_v1)",
    )
    parser.add_argument(
        "--min-trades",
        type=int,
        default=100,
        help="Minimum resolved trades required to train (default: 100)",
    )
    args = parser.parse_args()

    csv_files = sorted(glob(args.input))
    if not csv_files:
        _log.error(f"No CSV files found matching {args.input!r}")
        sys.exit(1)

    _log.info(f"Found {len(csv_files)} trade CSV files")

    dfs = []
    for f in csv_files:
        try:
            df = pd.read_csv(f)
            if "result" in df.columns:
                dfs.append(df)
        except Exception as e:
            _log.warning(f"Could not read {f}: {e}")

    if not dfs:
        _log.error("No valid trade CSVs found")
        sys.exit(1)

    merged = pd.concat(dfs, ignore_index=True)
    n_total = len(merged)
    n_win = (merged["result"] == "WIN").sum()
    n_loss = (merged["result"] == "LOSS").sum()
    n_other = n_total - n_win - n_loss

    _log.info(f"Merged {n_total} trades ({n_win} WIN, {n_loss} LOSS, {n_other} other)")

    if n_win + n_loss < args.min_trades:
        _log.error(
            f"Only {n_win + n_loss} resolved trades, need {args.min_trades}. "
            "Run backtest with more data first."
        )
        sys.exit(1)

    merged_path = "data/training_data_merged.csv"
    merged.to_csv(merged_path, index=False)
    _log.info(f"Training data saved to {merged_path}")

    scorer = TradeScorer()
    metrics = scorer.train(merged_path)
    _log.info("Training metrics:")
    for k, v in metrics.items():
        _log.info(f"  {k}: {v}")

    # Feature importance
    if scorer.model is not None and hasattr(scorer.model, "feature_importances_"):
        importances = scorer.model.feature_importances_
        feat_names = scorer.feature_names
        pairs = sorted(
            zip(feat_names, importances), key=lambda x: -x[1]
        )
        _log.info("Feature importance (top-10):")
        for name, imp in pairs[:10]:
            _log.info(f"  {name:30s}  {imp:.4f}")

    scorer.save(args.output)
    _log.info(f"Model saved to {args.output}.json + {args.output}.meta.json")


if __name__ == "__main__":
    main()
