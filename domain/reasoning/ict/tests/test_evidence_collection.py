from datetime import datetime

from domain.ontology.expansion import Expansion, ExpansionDirection
from domain.ontology.structure_event import (
    StructureDirection,
    StructureEvent,
    StructureEventType,
)
from domain.reasoning.ict.ict_reasoning_model import ICTReasoningModel
from domain.reasoning.structural_context import StructuralContext


def expansion():

    return Expansion(
        base_swing_index=1,
        confirmation_event_index=2,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        start_price=100,
        end_price=110,
        direction=ExpansionDirection.BULLISH,
    )


def bos():

    return StructureEvent(
        event_id=1,
        event_type=StructureEventType.BOS,
        direction=StructureDirection.BULLISH,
        timestamp=datetime.now(),
        candle_index=10,
        broken_swing_index=4,
        base_swing_index=3,
        price=110,
        displacement=5,
    )


def choch():

    return StructureEvent(
        event_id=2,
        event_type=StructureEventType.CHOCH,
        direction=StructureDirection.BEARISH,
        timestamp=datetime.now(),
        candle_index=20,
        broken_swing_index=5,
        base_swing_index=4,
        price=105,
        displacement=6,
    )


def context():

    return StructuralContext(
        context="Bullish Expansion",
        dominant_expansion="BULLISH",
        protected_structure="Present",
        latest_structure_event="BOS",
        observations=(),
        confidence_notes=(),
    )


def test_collect_supporting_evidence():

    model = ICTReasoningModel()

    evidence = model._collect_supporting_evidence(
        market=None,
        context=context(),
        active_expansion=expansion(),
        latest_structure_event=bos(),
        protected_structure=object(),
    )

    assert "Bullish Expansion" in evidence
    assert "Protected Structure Present" in evidence


def test_collect_counter_evidence_for_choch():

    model = ICTReasoningModel()

    evidence = model._collect_counter_evidence(
        market=None,
        context=context(),
        active_expansion=expansion(),
        latest_structure_event=choch(),
        protected_structure=object(),
    )

    assert "Recent CHOCH" in evidence


def test_no_counter_evidence_for_bos():

    model = ICTReasoningModel()

    evidence = model._collect_counter_evidence(
        market=None,
        context=context(),
        active_expansion=expansion(),
        latest_structure_event=bos(),
        protected_structure=object(),
    )

    assert evidence == ()