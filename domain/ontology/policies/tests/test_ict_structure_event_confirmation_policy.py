import pytest
from datetime import datetime

from domain.market_observation.market_observation import MarketObservation
from domain.market_observation.observation_history import ObservationHistory
from domain.market_observation.observation_metadata import ObservationMetadata

from domain.ontology.structure_event import (
    StructureEventType,
    StructureDirection,
)

from domain.ontology.candidates.structure_event_candidate import (
    StructureEventCandidate,
)

from domain.ontology.policies.ict.ict_structure_event_confirmation_policy import (
    ICTStructureEventConfirmationPolicy,
)

from domain.ontology.policies.structure_event_confirmation_result import (
    StructureEventConfirmationResult,
)


def create_history():

    observations = (
        MarketObservation(
            timestamp=datetime(2026, 1, 1, 9, 15),
            open=100,
            high=105,
            low=99,
            close=103,
            volume=100,
        ),
        MarketObservation(
            timestamp=datetime(2026, 1, 1, 9, 30),
            open=103,
            high=106,
            low=102,
            close=105,
            volume=120,
        ),
    )

    metadata = ObservationMetadata(
        symbol="TEST",
        timeframe="15m",
        start_time=observations[0].timestamp,
        end_time=observations[-1].timestamp,
        observation_count=len(observations),
    )

    return ObservationHistory(
        observations=observations,
        metadata=metadata,
    )


def test_confirm_returns_confirmation_result():

    candidate = StructureEventCandidate(
        event_type=StructureEventType.BOS,
        direction=StructureDirection.BULLISH,
        timestamp=datetime.now(),
        candle_index=1,
        broken_swing_index=0,
        base_swing_index=0,
        price=105,
        displacement=2.5,
    )

    policy = ICTStructureEventConfirmationPolicy()

    result = policy.confirm(
        candidate,
        create_history(),
    )

    assert result.confirmed is True


def test_confirmation_index_matches_candidate():

    candidate = StructureEventCandidate(
        event_type=StructureEventType.BOS,
        direction=StructureDirection.BULLISH,
        timestamp=datetime.now(),
        candle_index=1,
        broken_swing_index=0,
        base_swing_index=0,
        price=105,
        displacement=2.5,
    )

    policy = ICTStructureEventConfirmationPolicy()

    result = policy.confirm(
        candidate,
        create_history(),
    )

    assert result.confirmation_index == candidate.candle_index


def test_returns_confirmation_result_object():

    candidate = StructureEventCandidate(
        event_type=StructureEventType.CHOCH,
        direction=StructureDirection.BEARISH,
        timestamp=datetime.now(),
        candle_index=1,
        broken_swing_index=0,
        base_swing_index=0,
        price=100,
        displacement=1.8,
    )

    policy = ICTStructureEventConfirmationPolicy()

    result = policy.confirm(
        candidate,
        create_history(),
    )

    assert isinstance(
        result,
        StructureEventConfirmationResult,
    )


def test_requires_history():

    candidate = StructureEventCandidate(
        event_type=StructureEventType.BOS,
        direction=StructureDirection.BULLISH,
        timestamp=datetime.now(),
        candle_index=1,
        broken_swing_index=0,
        base_swing_index=0,
        price=100,
        displacement=2,
    )

    policy = ICTStructureEventConfirmationPolicy()

    with pytest.raises(ValueError):
        policy.confirm(candidate, None)