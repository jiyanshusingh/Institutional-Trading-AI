from architecture.selection.selection_policy import SelectionPolicy


class ICTOriginSelectionPolicy(SelectionPolicy):

    def select(
        self,
        candidates
    ):

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda candidate: candidate.subject
        )