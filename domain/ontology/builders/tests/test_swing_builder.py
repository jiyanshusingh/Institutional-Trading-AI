from datetime import datetime

from domain.market_observation.market_observation import MarketObservation
from domain.market_observation.observation_history import ObservationHistory
from domain.market_observation.observation_metadata import ObservationMetadata

from domain.ontology.builders.swing_builder import SwingBuilder

from domain.ontology.candidates.ict.ict_swing_candidate_detector import (
    ICTSwingCandidateDetector,
)

from domain.ontology.policies.ict.ict_swing_confirmation_policy import (
    ICTSwingConfirmationPolicy,
)
from domain.ontology.calculations.swing_strength_calculator import (
    SwingStrengthCalculator,
)
from domain.ontology.swing import Swing


def create_history():

    observations = (

        MarketObservation(
            timestamp=datetime(2026, 1, 1, 9, 15),
            open=100,
            high=101,
            low=99,
            close=100,
            volume=100,
        ),

        MarketObservation(
            timestamp=datetime(2026, 1, 1, 9, 30),
            open=100,
            high=110,
            low=98,
            close=109,
            volume=100,
        ),

        MarketObservation(
            timestamp=datetime(2026, 1, 1, 9, 45),
            open=101,
            high=102,
            low=97,
            close=100,
            volume=100,
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


def create_builder():

    detector = ICTSwingCandidateDetector(
        lookback=1,
    )

    policy = ICTSwingConfirmationPolicy(
        strength_calculator=SwingStrengthCalculator(),
        lookback=1,
    )
    return SwingBuilder(
        detector=detector,
        confirmation_policy=policy,
    )


def test_builder_returns_tuple():

    builder = create_builder()

    swings = builder.build(
        create_history(),
    )

    assert isinstance(swings, tuple)


def test_builder_returns_swing_objects():

    builder = create_builder()

    swings = builder.build(
        create_history(),
    )

    assert all(
        isinstance(swing, Swing)
        for swing in swings
    )


def test_builder_creates_confirmed_swing():

    builder = create_builder()

    swings = builder.build(
        create_history(),
    )

    assert len(swings) == 1

    swing = swings[0]

    assert swing.index == 1

    assert swing.confirmation_index == swing.index + 1

def test_builder_requires_history():

    import pytest

    builder = create_builder()

    with pytest.raises(Exception):

        builder.build(None)