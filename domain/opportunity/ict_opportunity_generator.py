from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from domain.opportunity.opportunity import Opportunity
from domain.opportunity.opportunity_generator import OpportunityGenerator
from domain.thesis.market_thesis import MarketThesis


class ICTOpportunityGenerator(OpportunityGenerator):
    """
    Version 1 ICT Opportunity Generator.

    Converts Market Theses into standardized
    Opportunity objects.
    """

    @property
    def generator_name(self) -> str:
        return "ICTOpportunityGenerator"

    @property
    def theory(self) -> str:
        return "ICT"

    @property
    def version(self) -> str:
        return "1.0"

    # ==========================================================
    # Public API
    # ==========================================================

    def generate(
        self,
        market_theses: tuple[MarketThesis, ...],
        objectives=None,
        constraints=None,
    ) -> tuple[Opportunity, ...]:

        opportunities = []

        for thesis in market_theses:

            opportunities.append(
                self._generate_opportunity(thesis)
            )

        return tuple(opportunities)

    # ==========================================================
    # Internal Decision Logic
    # ==========================================================

    def _generate_opportunity(
        self,
        thesis: MarketThesis,
    ) -> Opportunity:

        opportunity_type = self._determine_opportunity_type(
            thesis
        )

        direction = self._determine_direction(
            opportunity_type
        )

        priority = self._determine_priority(
            thesis
        )

        return Opportunity(
            opportunity_id=str(uuid4()),
            created_at=datetime.now(UTC),

            symbol=thesis.symbol,
            timeframe=thesis.timeframe,

            opportunity_type=opportunity_type,
            direction=direction,
            priority=priority,

            supporting_thesis_ids=(
                thesis.thesis_id,
            ),

            evidence_quality=thesis.uncertainty,

            reasoning_quality="HIGH",

            expected_structural_evolution=(
                thesis.expected_structural_evolution
            ),

            assumptions=thesis.assumptions,

            invalidation=thesis.invalidation,
        )

    # ==========================================================
    # Decision Rules
    # ==============================================================

    def _determine_opportunity_type(
        self,
        thesis: MarketThesis,
    ) -> str:

        claim = thesis.central_claim.lower()

        if (
            "bullish" in claim
            and thesis.uncertainty == "STRONG"
        ):
            return "LONG"

        if (
            "bearish" in claim
            and thesis.uncertainty == "STRONG"
        ):
            return "SHORT"

        return "WAIT"

    def _determine_direction(
        self,
        opportunity_type: str,
    ) -> str:

        if opportunity_type == "LONG":
            return "LONG"

        if opportunity_type == "SHORT":
            return "SHORT"

        return "NONE"

    def _determine_priority(
        self,
        thesis: MarketThesis,
    ) -> str:

        if thesis.uncertainty == "STRONG":
            return "HIGH"

        if thesis.uncertainty == "MODERATE":
            return "MEDIUM"

        return "LOW"