from assessments.structural.structural_assessment import StructuralAssessment
from assessments.structural.structural_state import StructuralState


class StructuralAssessmentPolicy:

    def __init__(self):

        self.rules = [

            ContinuationRule()

        ]

    def assess(self, observations):

        for rule in self.rules:

            assessment = rule.evaluate(observations)

            if assessment is not None:

                return assessment

        return StructuralAssessment(
            state=StructuralState.UNKNOWN,
            evidence=()
        )