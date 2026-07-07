"""
ICT Structure Event Candidate Detector

Theory 1.0

Commit 2

Implements Bullish BOS candidate detection.
"""

from __future__ import annotations

from domain.market_observation.observation_history import (
    ObservationHistory,
)

from domain.ontology.swing import Swing
from domain.ontology.swing_type import SwingType

from domain.ontology.structure_event import (
    StructureEventType,
    StructureDirection,
)

from domain.ontology.candidates.structure_event_candidate import (
    StructureEventCandidate,
)

from ..structure_event_candidate_detector import (
    StructureEventCandidateDetector,
)


class ICTStructureEventCandidateDetector(
    StructureEventCandidateDetector
):

    def detect(
        self,
        observation_history: ObservationHistory,
        swings: tuple[Swing, ...],
    ) -> tuple[StructureEventCandidate, ...]:

        if observation_history is None:
            raise ValueError(
                "ObservationHistory is required."
            )

        if swings is None:
            raise ValueError(
                "Confirmed swings are required."
            )

        if len(swings) == 0:
            return ()

        candidates: list[StructureEventCandidate] = []

        candidates.extend(
            self._detect_bullish_bos(
                observation_history,
                swings,
            )
        )

        #
        # Commit 3
        #
        # candidates.extend(
        #     self._detect_bearish_bos(...)
        # )

        return tuple(candidates)

    # ---------------------------------------------------------
    # Bullish BOS
    # ---------------------------------------------------------

    def _detect_bullish_bos(
        self,
        observation_history: ObservationHistory,
        swings: tuple[Swing, ...],
    ) -> list[StructureEventCandidate]:

        candidates: list[StructureEventCandidate] = []

        observations = observation_history.observations

        for swing in swings:

            if swing.swing_type != SwingType.HIGH:
                continue

            start = swing.confirmation_index + 1

            for candle_index in range(
                start,
                len(observations),
            ):

                candle = observations[candle_index]

                #
                # BOS Rule
                #
                if candle.close <= swing.price:
                    continue

                candidates.append(

                    StructureEventCandidate(

                        event_type=StructureEventType.BOS,

                        direction=StructureDirection.BULLISH,

                        timestamp=candle.timestamp,

                        candle_index=candle_index,

                        broken_swing_index=swing.index,

                        base_swing_index=swing.index,

                        price=candle.close,

                        displacement=(
                            candle.close - swing.price
                        ),

                    )

                )

                #
                # First break wins.
                #
                break

        return candidates