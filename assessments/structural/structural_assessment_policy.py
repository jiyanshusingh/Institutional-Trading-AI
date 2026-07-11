from assessments.structural.structural_assessment import StructuralAssessment
from assessments.structural.structural_state import StructuralState
from assessments.structural.rules.continuation_rule import ContinuationRule


class StructuralAssessmentPolicy:

    def __init__(self):

        self.rules = [

            ContinuationRule()

        ]

    def assess(self, configuration):

        for rule in self.rules:

            assessment = rule.evaluate(configuration)

            if assessment is not None:

                return assessment

        return StructuralAssessment(
            state=StructuralState.UNKNOWN,
            evidence=()
        )