from dataclasses import FrozenInstanceError

import pytest

from domain.ontology.policies.origin_region_confirmation_result import (
    OriginRegionConfirmationResult,
)


def test_create_confirmed_result():

    result = OriginRegionConfirmationResult(
        confirmed=True,
        confirmation_index=5,
    )

    assert result.confirmed is True
    assert result.confirmation_index == 5


def test_create_rejected_result():

    result = OriginRegionConfirmationResult(
        confirmed=False,
        reason="Rejected",
    )

    assert result.confirmed is False
    assert result.reason == "Rejected"


def test_confirmed_requires_confirmation_index():

    with pytest.raises(ValueError):

        OriginRegionConfirmationResult(
            confirmed=True,
        )


def test_rejected_cannot_have_confirmation_index():

    with pytest.raises(ValueError):

        OriginRegionConfirmationResult(
            confirmed=False,
            confirmation_index=1,
        )


def test_result_is_immutable():

    result = OriginRegionConfirmationResult(
        confirmed=True,
        confirmation_index=1,
    )

    with pytest.raises(FrozenInstanceError):
        result.confirmed = False