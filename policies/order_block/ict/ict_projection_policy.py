from policies.order_block.base_projection_policy import (
    ProjectionPolicy
)


class ICTProjectionPolicy(ProjectionPolicy):

    def select(
        self,
        candidates
    ):

        for candidate in candidates:

            if candidate.metadata["projection"] == "BODY":
                return candidate

        return candidates[0]