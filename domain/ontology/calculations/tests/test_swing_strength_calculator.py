import pytest

from domain.ontology.calculations.swing_strength_calculator import (
    SwingStrengthCalculator,
)


def test_zero_atr_returns_zero():

    calculator = SwingStrengthCalculator()

    strength = calculator.calculate(
        high=105,
        low=100,
        atr=0,
    )

    assert strength == 0.0


def test_calculate_strength():

    calculator = SwingStrengthCalculator()

    strength = calculator.calculate(
        high=110,
        low=100,
        atr=2,
    )

    assert strength == 5.0


def test_rounds_to_two_decimals():

    calculator = SwingStrengthCalculator()

    strength = calculator.calculate(
        high=111,
        low=100,
        atr=3,
    )

    assert strength == 3.67


def test_negative_atr_not_allowed():

    calculator = SwingStrengthCalculator()

    with pytest.raises(ValueError):

        calculator.calculate(
            high=105,
            low=100,
            atr=-1,
        )


def test_high_must_be_above_low():

    calculator = SwingStrengthCalculator()

    with pytest.raises(ValueError):

        calculator.calculate(
            high=100,
            low=105,
            atr=2,
        )