from dataclasses import FrozenInstanceError

import pytest

from domain.ontology.policies.fair_value_gap_confirmation_result import (
    FairValueGapConfirmationResult,
)


def test_create_confirmed_result():

    result = FairValueGapConfirmationResult(
        confirmed=True,
        confirmation_index=1,
    )

    assert result.confirmed
    assert result.confirmation_index == 1


def test_create_rejected_result():

    result = FairValueGapConfirmationResult(
        confirmed=False,
        reason="Rejected",
    )

    assert not result.confirmed
    assert result.reason == "Rejected"


def test_confirmed_requires_confirmation_index():

    with pytest.raises(ValueError):

        FairValueGapConfirmationResult(
            confirmed=True,
        )


def test_rejected_cannot_have_confirmation_index():

    with pytest.raises(ValueError):

        FairValueGapConfirmationResult(
            confirmed=False,
            confirmation_index=1,
        )


def test_result_is_immutable():

    result = FairValueGapConfirmationResult(
        confirmed=True,
        confirmation_index=1,
    )

    with pytest.raises(FrozenInstanceError):
        result.confirmed = False