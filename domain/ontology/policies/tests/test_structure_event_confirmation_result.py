import pytest

from domain.ontology.policies.structure_event_confirmation_result import (
    StructureEventConfirmationResult,
)


def test_create_confirmed_result():

    result = StructureEventConfirmationResult(
        confirmed=True,
        confirmation_index=15,
    )

    assert result.confirmed is True
    assert result.confirmation_index == 15


def test_create_rejected_result():

    result = StructureEventConfirmationResult(
        confirmed=False,
        reason="Rejected",
    )

    assert result.confirmed is False
    assert result.reason == "Rejected"


def test_confirmed_requires_confirmation_index():

    with pytest.raises(ValueError):

        StructureEventConfirmationResult(
            confirmed=True,
        )


def test_rejected_cannot_have_confirmation_index():

    with pytest.raises(ValueError):

        StructureEventConfirmationResult(
            confirmed=False,
            confirmation_index=10,
        )


def test_result_is_immutable():

    result = StructureEventConfirmationResult(
        confirmed=True,
        confirmation_index=10,
    )

    with pytest.raises(Exception):
        result.confirmed = False