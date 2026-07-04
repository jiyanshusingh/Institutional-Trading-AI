"""
ICT Swing Candidate Detector

ICT Theory v1.0

Detects potential Swing candidates from an ObservationHistory.

This detector performs only local-extrema detection.

It does NOT:

- confirm swings
- evaluate displacement
- use ATR
- assign strength
"""

from domain.market_observation.observation_history import ObservationHistory
from domain.ontology.swing_type import SwingType

from ..swing_candidate import SwingCandidate
from ..swing_candidate_detector import SwingCandidateDetector


class ICTSwingCandidateDetector(SwingCandidateDetector):

    def __init__(self, lookback: int = 3):

        if lookback < 1:
            raise ValueError("Lookback must be at least 1.")

        self._lookback = lookback

    def detect(
        self,
        observation_history: ObservationHistory,
    ) -> tuple[SwingCandidate, ...]:

        observations = observation_history.observations

        candidates = []

        for i in range(
            self._lookback,
            len(observations) - self._lookback,
        ):

            window = observations[
                i - self._lookback:
                i + self._lookback + 1
            ]

            current = observations[i]

            window_highs = [
                candle.high
                for candle in window
            ]

            window_lows = [
                candle.low
                for candle in window
            ]

            highest = max(window_highs)
            lowest = min(window_lows)

            #
            # Unique Swing High
            #

            if (
                current.high == highest
                and window_highs.count(highest) == 1
            ):

                candidates.append(
                    SwingCandidate(
                        index=i,
                        timestamp=current.timestamp,
                        price=current.high,
                        swing_type=SwingType.HIGH,
                    )
                )

            #
            # Unique Swing Low
            #

            if (
                current.low == lowest
                and window_lows.count(lowest) == 1
            ):

                candidates.append(
                    SwingCandidate(
                        index=i,
                        timestamp=current.timestamp,
                        price=current.low,
                        swing_type=SwingType.LOW,
                    )
                )

        return tuple(candidates)