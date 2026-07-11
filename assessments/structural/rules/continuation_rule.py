from assessments.structural.structural_assessment import StructuralAssessment
from assessments.structural.structural_state import StructuralState
from assessments.structural.rules.base_rule import StructuralRule
from domain.ontology.structure_event import StructureDirection


class ContinuationRule(StructuralRule):

    def evaluate(self, configuration):

        latest = configuration.latest_expansion()

        if latest is None:
            return None

        events = configuration.structure_events_after(
            latest.confirmation_event_index
        )

        for event in events:

            if not event.valid:
                continue

            if event.event_type.value != "CHOCH":
                continue

            if (
                latest.direction == StructureDirection.BULLISH
                and event.direction == StructureDirection.BEARISH
            ):
                return None

            if (
                latest.direction == StructureDirection.BEARISH
                and event.direction == StructureDirection.BULLISH
            ):
                return None

        if latest.direction == StructureDirection.BULLISH:

            return StructuralAssessment(
                state=StructuralState.BULLISH_CONTINUATION,
                evidence=(latest,)
            )

        if latest.direction == StructureDirection.BEARISH:

            return StructuralAssessment(
                state=StructuralState.BEARISH_CONTINUATION,
                evidence=(latest,)
            )

        return None