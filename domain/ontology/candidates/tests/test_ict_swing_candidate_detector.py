from datetime import datetime

from domain.market_observation.market_observation import MarketObservation
from domain.market_observation.observation_history import ObservationHistory
from domain.market_observation.observation_metadata import ObservationMetadata

from domain.ontology.candidates.ict.ict_swing_candidate_detector import (
    ICTSwingCandidateDetector,
)

from domain.ontology.swing_type import SwingType


def create_history(highs, lows):

    observations = []

    for i in range(len(highs)):

        observations.append(
            MarketObservation(
                timestamp=datetime(2026, 1, 1, 9, 15 + i),
                open=lows[i],
                high=highs[i],
                low=lows[i],
                close=highs[i],
                volume=100,
            )
        )

    metadata = ObservationMetadata(
        symbol="TEST",
        timeframe="1m",
        start_time=observations[0].timestamp,
        end_time=observations[-1].timestamp,
        observation_count=len(observations),
    )

    return ObservationHistory(
        observations=tuple(observations),
        metadata=metadata,
    )


def test_detect_single_swing_high():

    history = create_history(

        highs=[1, 2, 5, 2, 1],

        lows=[0, 1, 2, 1, 0],
    )

    detector = ICTSwingCandidateDetector(
        lookback=2,
    )

    candidates = detector.detect(history)

    assert len(candidates) == 1

    candidate = candidates[0]

    assert candidate.index == 2
    assert candidate.price == 5
    assert candidate.swing_type == SwingType.HIGH


def test_detect_single_swing_low():

    history = create_history(

        highs=[5, 4, 3, 4, 5],

        lows=[4, 3, 1, 3, 4],
    )

    detector = ICTSwingCandidateDetector(
        lookback=2,
    )

    candidates = detector.detect(history)

    assert len(candidates) == 1

    candidate = candidates[0]

    assert candidate.index == 2
    assert candidate.price == 1
    assert candidate.swing_type == SwingType.LOW


def test_detect_high_and_low():

    history = create_history(

        highs=[11, 13, 16, 13, 11, 15, 12],

        lows=[10, 9, 11, 8, 10, 9, 12],
    )

    detector = ICTSwingCandidateDetector(
        lookback=1,
    )

    candidates = detector.detect(history)

    assert len(candidates) >= 2


def test_no_candidates():

    history = create_history(

        highs=[1, 1, 1, 1, 1],

        lows=[1, 1, 1, 1, 1],
    )

    detector = ICTSwingCandidateDetector(
        lookback=1,
    )

    candidates = detector.detect(history)

    assert len(candidates) == 0


def test_invalid_lookback():

    import pytest

    with pytest.raises(ValueError):

        ICTSwingCandidateDetector(
            lookback=0,
        )


def test_returns_tuple():

    history = create_history(

        highs=[1, 2, 5, 2, 1],

        lows=[0, 1, 2, 1, 0],
    )

    detector = ICTSwingCandidateDetector()

    candidates = detector.detect(history)

    assert isinstance(candidates, tuple)