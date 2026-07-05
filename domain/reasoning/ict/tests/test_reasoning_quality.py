from datetime import UTC, datetime

from domain.reasoning.evidence_assessment import EvidenceAssessment
from domain.reasoning.ict.ict_reasoning_model import ICTReasoningModel
from domain.thesis.market_thesis import MarketThesis


def make_thesis() -> MarketThesis:

    return MarketThesis(
        thesis_id="1",
        created_at=datetime.now(UTC),

        symbol="RELIANCE",
        timeframe="15m",

        reasoning_model="ICTReasoningModel",
        theory="ICT",
        version="1.0",

        market_regime="Bullish Expansion",
        session="UNKNOWN",

        objectives=(),

        central_claim=(
            "Bullish continuation is currently the most "
            "supported structural hypothesis."
        ),

        supporting_evidence=(
            "Bullish Expansion",
            "Bullish BOS",
            "Protected Structure Present",
        ),

        counter_evidence=(),

        assumptions=(
            "Current structural context remains valid.",
        ),

        expected_structural_evolution=(
            "Continuation of the bullish structural "
            "expansion is currently the most justified "
            "expected evolution."
        ),

        invalidation=(
            "Confirmed bearish CHOCH.",
        ),

        uncertainty="STRONG",
    )


def strong_evidence() -> EvidenceAssessment:

    return EvidenceAssessment(
        level="STRONG",
        supporting_count=3,
        counter_count=0,
        rationale="Strong supporting evidence.",
    )


def weak_evidence() -> EvidenceAssessment:

    return EvidenceAssessment(
        level="WEAK",
        supporting_count=1,
        counter_count=2,
        rationale="Weak supporting evidence.",
    )


def test_high_reasoning_quality():

    model = ICTReasoningModel()

    quality = model._assess_reasoning_quality(
        make_thesis(),
        strong_evidence(),
    )

    assert quality.level == "HIGH"


def test_weak_evidence_reduces_reasoning_quality():

    model = ICTReasoningModel()

    quality = model._assess_reasoning_quality(
        make_thesis(),
        weak_evidence(),
    )

    assert quality.level == "MEDIUM"


def test_reasoning_is_complete():

    model = ICTReasoningModel()

    quality = model._assess_reasoning_quality(
        make_thesis(),
        strong_evidence(),
    )

    assert quality.complete


def test_reasoning_is_explainable():

    model = ICTReasoningModel()

    quality = model._assess_reasoning_quality(
        make_thesis(),
        strong_evidence(),
    )

    assert quality.explainable


def test_reasoning_is_falsifiable():

    model = ICTReasoningModel()

    quality = model._assess_reasoning_quality(
        make_thesis(),
        strong_evidence(),
    )

    assert quality.falsifiable


def test_reasoning_is_internally_consistent():

    model = ICTReasoningModel()

    quality = model._assess_reasoning_quality(
        make_thesis(),
        strong_evidence(),
    )

    assert quality.internally_consistent


def test_reasoning_is_evidence_supported():

    model = ICTReasoningModel()

    quality = model._assess_reasoning_quality(
        make_thesis(),
        strong_evidence(),
    )

    assert quality.evidence_supported


def test_reasoning_score():

    model = ICTReasoningModel()

    quality = model._assess_reasoning_quality(
        make_thesis(),
        strong_evidence(),
    )

    assert quality.score == 5