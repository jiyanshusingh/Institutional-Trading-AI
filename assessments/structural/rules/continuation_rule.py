from assessments.structural.structural_assessment import StructuralAssessment
from assessments.structural.structural_state import StructuralState
from assessments.structural.rules.base_rule import StructuralRule


class ContinuationRule(StructuralRule):

    def evaluate(self, configuration):

        latest = configuration.latest_expansion()

        if latest is None:
            return None

        events = configuration.structure_events_after(
            latest.end_index
        )

        for event in events:

            # Ignore invalid events
            if not event.valid:
                continue

            # We only care about CHOCH
            if event.event_type != "CHOCH":
                continue

            # Bullish continuation is broken
            if (
                latest.direction == "Bullish"
                and event.direction == "Bearish"
            ):
                return None

            # Bearish continuation is broken
            if (
                latest.direction == "Bearish"
                and event.direction == "Bullish"
            ):
                return None

        # No opposite CHOCH found

        if latest.direction == "Bullish":

            return StructuralAssessment(
                state=StructuralState.BULLISH_CONTINUATION,
                evidence=(latest,)
            )

        if latest.direction == "Bearish":

            return StructuralAssessment(
                state=StructuralState.BEARISH_CONTINUATION,
                evidence=(latest,)
            )

        return None