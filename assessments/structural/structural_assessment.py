from dataclasses import dataclass


@dataclass(frozen=True)
class StructuralAssessment:

    state: StructuralState

    evidence: tuple