from datetime import datetime

from domain.ontology.expansion import Expansion, ExpansionDirection
from domain.ontology.structure_event import (
    StructureDirection,
    StructureEvent,
    StructureEventType,
)
from domain.reasoning.ict.ict_reasoning_model import ICTReasoningModel


def bullish_expansion():

    return Expansion(
        base_swing_index=1,
        confirmation_event_index=2,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        start_price=100,
        end_price=110,
        direction=ExpansionDirection.BULLISH,
    )


def bearish_expansion():

    return Expansion(
        base_swing_index=1,
        confirmation_event_index=2,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        start_price=110,
        end_price=100,
        direction=ExpansionDirection.BEARISH,
    )


def bullish_bos():

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


def bearish_choch():

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


def test_no_expansion_is_indeterminate():

    model = ICTReasoningModel()

    context = model._determine_structural_context(
        None,
        None,
        None,
    )

    assert context.context == "Indeterminate"


def test_bullish_expansion_context():

    model = ICTReasoningModel()

    context = model._determine_structural_context(
        bullish_expansion(),
        bullish_bos(),
        object(),
    )

    assert context.context == "Bullish Expansion"


def test_bearish_expansion_context():

    model = ICTReasoningModel()

    context = model._determine_structural_context(
        bearish_expansion(),
        None,
        object(),
    )

    assert context.context == "Bearish Expansion"


def test_choch_creates_transition():

    model = ICTReasoningModel()

    context = model._determine_structural_context(
        bullish_expansion(),
        bearish_choch(),
        object(),
    )

    assert context.context == "Transition"