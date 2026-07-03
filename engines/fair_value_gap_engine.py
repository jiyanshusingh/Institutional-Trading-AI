from policies.fair_value_gap.base_fvg_policy import (
    FairValueGapPolicy
)


class FairValueGapEngine:

    def __init__(

        self,

        configuration,

        policy: FairValueGapPolicy

    ):

        self.configuration = configuration

        self.policy = policy

        self.fair_value_gaps = []

    def build(self):

        self.fair_value_gaps = list(

            self.policy.detect(

                self.configuration

            )

        )

        return tuple(self.fair_value_gaps)