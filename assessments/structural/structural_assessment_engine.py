from assessments.structural.structural_assessment_policy import (
    StructuralAssessmentPolicy
)


class StructuralAssessmentEngine:

    def __init__(self):

        self.policy = StructuralAssessmentPolicy()

    def assess(
        self,
        configuration
    ):

        return self.policy.assess(
            configuration
        )