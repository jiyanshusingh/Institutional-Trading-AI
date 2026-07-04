from datetime import datetime

from domain.market_observation.market_observation import MarketObservation
from domain.market_observation.observation_history import ObservationHistory
from domain.market_observation.observation_metadata import ObservationMetadata

from domain.ontology.candidates.swing_candidate import SwingCandidate
from domain.ontology.swing_type import SwingType

from domain.ontology.policies.ict.ict_swing_confirmation_policy import (
    ICTSwingConfirmationPolicy,
)
from domain.ontology.calculations.swing_strength_calculator import (
    SwingStrengthCalculator,
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

    history = create_history()

    candidate = SwingCandidate(
        index=0,
        timestamp=history.first.timestamp,
        price=105,
        swing_type=SwingType.HIGH,
    )

    policy = ICTSwingConfirmationPolicy(
        strength_calculator=SwingStrengthCalculator(),
        lookback=1,
    )
    result = policy.confirm(
        candidate,
        history,
    )

    assert result.confirmed is True


def test_confirmation_index_matches_candidate():

    history = create_history()

    candidate = SwingCandidate(
        index=0,
        timestamp=history.first.timestamp,
        price=105,
        swing_type=SwingType.HIGH,
    )

    policy = ICTSwingConfirmationPolicy(
        strength_calculator=SwingStrengthCalculator(),
        lookback=1,
    )

    result = policy.confirm(
        candidate,
        history,
    )

    assert result.confirmed is True
    assert result.confirmation_index == 1


def test_returns_confirmation_result_object():

    history = create_history()

    candidate = SwingCandidate(
        index=2,
        timestamp=datetime.now(),
        price=100,
        swing_type=SwingType.LOW,
    )

    policy = ICTSwingConfirmationPolicy(
        strength_calculator=SwingStrengthCalculator(),
        lookback=1,
    )
    result = policy.confirm(
        candidate,
        history,
    )

    assert result.__class__.__name__ == "SwingConfirmationResult"
    
def test_reject_when_future_confirmation_not_possible():

    history = create_history()

    candidate = SwingCandidate(
        index=0,
        timestamp=history.first.timestamp,
        price=105,
        swing_type=SwingType.HIGH,
    )

    policy = ICTSwingConfirmationPolicy(
        strength_calculator=SwingStrengthCalculator(),
        lookback=10,
    )

    result = policy.confirm(
        candidate,
        history,
    )

    assert result.confirmed is False
    assert result.confirmation_index is None