class PositionEngine:

    def calculate(
        self,
        entry,
        stoploss,
        capital,
        risk_percent=1
    ):

        risk_amount = capital * (risk_percent / 100)

        risk_per_share = abs(entry - stoploss)

        quantity = int(risk_amount / risk_per_share)

        investment = quantity * entry

        return {
            "Capital": capital,
            "RiskAmount": round(risk_amount, 2),
            "Quantity": quantity,
            "Investment": round(investment, 2)
        }