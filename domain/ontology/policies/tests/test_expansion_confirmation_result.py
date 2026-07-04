from dataclasses import FrozenInstanceError

import pytest

from domain.ontology.policies.expansion_confirmation_result import (
    ExpansionConfirmationResult,
)


def test_create_confirmed_result():

    result = ExpansionConfirmationResult(
        confirmed=True,
        confirmation_index=10,
    )

    assert result.confirmed is True
    assert result.confirmation_index == 10


def test_create_rejected_result():

    result = ExpansionConfirmationResult(
        confirmed=False,
        reason="Rejected",
    )

    assert result.confirmed is False
    assert result.reason == "Rejected"


def test_confirmed_requires_confirmation_index():

    with pytest.raises(ValueError):

        ExpansionConfirmationResult(
            confirmed=True,
        )


def test_rejected_cannot_have_confirmation_index():

    with pytest.raises(ValueError):

        ExpansionConfirmationResult(
            confirmed=False,
            confirmation_index=5,
        )


def test_result_is_immutable():

    result = ExpansionConfirmationResult(
        confirmed=True,
        confirmation_index=1,
    )

    with pytest.raises(FrozenInstanceError):
        result.confirmed = False