from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:

    id: int

    subject: object

    metadata: dict