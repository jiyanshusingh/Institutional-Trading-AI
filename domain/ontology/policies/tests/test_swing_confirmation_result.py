import pytest

from domain.ontology.policies.swing_confirmation_result import (
    SwingConfirmationResult,
)


def test_create_confirmed_result():

    result = SwingConfirmationResult(
        confirmed=True,
        confirmation_index=15,
    )

    assert result.confirmed is True
    assert result.confirmation_index == 15
    assert result.reason is None


def test_create_rejected_result():

    result = SwingConfirmationResult(
        confirmed=False,
        reason="ATR below threshold",
    )

    assert result.confirmed is False
    assert result.confirmation_index is None
    assert result.reason == "ATR below threshold"


def test_confirmed_requires_confirmation_index():

    with pytest.raises(ValueError):

        SwingConfirmationResult(
            confirmed=True,
            confirmation_index=None,
        )


def test_rejected_cannot_have_confirmation_index():

    with pytest.raises(ValueError):

        SwingConfirmationResult(
            confirmed=False,
            confirmation_index=10,
        )


def test_result_is_immutable():

    result = SwingConfirmationResult(
        confirmed=True,
        confirmation_index=5,
    )

    with pytest.raises(Exception):
        result.confirmed = False