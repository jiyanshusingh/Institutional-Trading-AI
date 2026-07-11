from __future__ import annotations
from datetime import UTC, datetime
from uuid import uuid4
from domain.reasoning.contracts.reasoning_model import ReasoningModel
from domain.reasoning.structural_context import StructuralContext
from domain.thesis.market_thesis import MarketThesis
from domain.ontology.expansion import ExpansionDirection
from domain.ontology.structure_event import StructureEventType
from domain.reasoning.evidence_assessment import EvidenceAssessment
from domain.reasoning.reasoning_quality import ReasoningQuality

class ICTReasoningModel(ReasoningModel):
    """
    Version 1 ICT Reasoning Model.

    Converts a CanonicalMarketModel into a single explainable
    MarketThesis.
    """

    @property
    def model_name(self) -> str:
        return "ICTReasoningModel"

    @property
    def theory(self) -> str:
        return "ICT"

    @property
    def version(self) -> str:
        return "1.0"

    # ==============================================================
    # Public API
    # ==============================================================

    def construct_market_theses(
        self,
        market,
        objectives=None,
        constraints=None,
    ) -> tuple[MarketThesis, ...]:

        active_expansion = self._determine_active_expansion(market)

        latest_structure_event = self._determine_latest_structure_event(market)

        protected_structure = self._determine_protected_structure(market)

        structural_context = self._determine_structural_context(
            active_expansion,
            latest_structure_event,
            protected_structure,
        )

        supporting_evidence = self._collect_supporting_evidence(
            market,
            structural_context,
            active_expansion,
            latest_structure_event,
            protected_structure,
        )

        counter_evidence = self._collect_counter_evidence(
            market,
            structural_context,
            active_expansion,
            latest_structure_event,
            protected_structure,
        )

        # ----------------------------------------------------------
        # Assess evidence quality
        # ----------------------------------------------------------

        evidence_assessment = self._assess_evidence_quality(
            supporting_evidence,
            counter_evidence,
        )

        # ----------------------------------------------------------
        # Construct thesis
        # ----------------------------------------------------------

        thesis = self._construct_market_thesis(
            market=market,
            context=structural_context,
            supporting_evidence=supporting_evidence,
            counter_evidence=counter_evidence,
            evidence_assessment=evidence_assessment,
            objectives=objectives,
        )
        
        reasoning_quality = self._assess_reasoning_quality(
            thesis,
            evidence_assessment,
        )

        return (thesis,)
    # ==============================================================
    # Semantic Queries
    # ==============================================================

    def _determine_active_expansion(self, market):

        if not market.expansions:
            return None

        return market.expansions[-1]

    def _determine_latest_structure_event(self, market):

        if not market.structure_events:
            return None

        return market.structure_events[-1]

    def _determine_protected_structure(self, market):

        if not market.protected_swings:
            return None

        return market.protected_swings[-1]

    # ==============================================================
    # Structural Reasoning
    # ==============================================================

    def _determine_structural_context(
        self,
        active_expansion,
        latest_structure_event,
        protected_structure,
    ) -> StructuralContext:

        # No expansion yet
        if active_expansion is None:
            context = "Indeterminate"

        # CHOCH overrides previous expansion
        elif (
            latest_structure_event is not None
            and latest_structure_event.event_type == StructureEventType.CHOCH
        ):
            context = "Transition"

        # Bullish Expansion
        elif active_expansion.direction == ExpansionDirection.BULLISH:
            context = "Bullish Expansion"

        # Bearish Expansion
        else:
            context = "Bearish Expansion"

        return StructuralContext(
            context=context,
            dominant_expansion=(
                active_expansion.direction.value
                if active_expansion is not None
                else "None"
            ),
            protected_structure=(
                "Present"
                if protected_structure is not None
                else "Absent"
            ),
            latest_structure_event=(
                latest_structure_event.event_type.value
                if latest_structure_event is not None
                else "None"
            ),
            observations=(),
            confidence_notes=(),
        )

    # ==============================================================
    # Evidence Collection
    # ==============================================================

    def _collect_supporting_evidence(
        self,
        market,
        context,
        active_expansion,
        latest_structure_event,
        protected_structure,
    ) -> tuple[str, ...]:

        evidence = []

        if active_expansion is not None:

            if active_expansion.is_bullish:
                evidence.append("Bullish Expansion")

            elif active_expansion.is_bearish:
                evidence.append("Bearish Expansion")

        if latest_structure_event is not None:
            direction_text = latest_structure_event.direction.value

            if active_expansion is not None:
                expansion_dir = (
                    "BULLISH" if active_expansion.is_bullish else "BEARISH"
                )
                if direction_text == expansion_dir:
                    evidence.append(
                        f"{direction_text} "
                        f"{latest_structure_event.event_type.value} "
                        f"(aligned with expansion)"
                    )
                else:
                    evidence.append(
                        f"{direction_text} "
                        f"{latest_structure_event.event_type.value} "
                        f"(counter-trend)"
                    )
            else:
                evidence.append(
                    f"{direction_text} "
                    f"{latest_structure_event.event_type.value}"
                )

        if protected_structure is not None:
            evidence.append("Protected Structure Present")

        return tuple(evidence)

    def _collect_counter_evidence(
        self,
        market,
        context,
        active_expansion,
        latest_structure_event,
        protected_structure,
    ) -> tuple[str, ...]:

        evidence = []

        if (
            latest_structure_event is not None
            and latest_structure_event.event_type == StructureEventType.CHOCH
        ):
            evidence.append("Recent CHOCH")

        if latest_structure_event is not None and active_expansion is not None:
            expansion_dir = (
                "BULLISH" if active_expansion.is_bullish else "BEARISH"
            )
            event_dir = latest_structure_event.direction.value
            if expansion_dir != event_dir:
                evidence.append(
                    f"Structure event contradicts expansion direction"
                )

        return tuple(evidence)
# ==============================================================
# Evidence Assessment
# ==============================================================
    def _assess_evidence_quality(
        self,
        supporting_evidence: tuple[str, ...],
        counter_evidence: tuple[str, ...],
    ) -> EvidenceAssessment:
        """
        Assess how well the current Market Thesis is supported
        by the available evidence.

        Version 1 uses simple deterministic rules.
        """

        supporting_count = len(supporting_evidence)
        counter_count = len(counter_evidence)

        if supporting_count >= 3 and counter_count == 0:

            level = "STRONG"

            rationale = (
                "Multiple independent observations support "
                "the current structural interpretation."
            )

        elif supporting_count >= 2 and counter_count <= 1:

            level = "MODERATE"

            rationale = (
                "Supporting evidence outweighs "
                "counter evidence."
            )

        else:

            level = "WEAK"

            rationale = (
                "The current thesis has limited support "
                "or significant contradictory evidence."
            )

        return EvidenceAssessment(
            level=level,
            supporting_count=supporting_count,
            counter_count=counter_count,
            rationale=rationale,
        )
    # ==============================================================
    # Reasoning Quality Assessment
    # ==============================================================
    
    def _assess_reasoning_quality(
        self,
        thesis: MarketThesis,
        evidence_assessment,
    ) -> ReasoningQuality:
        """
        Assess the quality of the reasoning used to construct
        the Market Thesis.

        Version 1 uses deterministic rule-based evaluation.
        """

        complete = (
            bool(thesis.central_claim)
            and bool(thesis.supporting_evidence)
            and bool(thesis.expected_structural_evolution)
            and bool(thesis.invalidation)
        )

        explainable = (
            len(thesis.supporting_evidence) > 0
        )

        falsifiable = thesis.is_falsifiable()

        internally_consistent = True

        evidence_supported = (
            evidence_assessment.level != "WEAK"
        )

        score = sum(
            (
                complete,
                explainable,
                falsifiable,
                internally_consistent,
                evidence_supported,
            )
        )

        if score == 5:
            level = "HIGH"

        elif score >= 3:
            level = "MEDIUM"

        else:
            level = "LOW"

        return ReasoningQuality(
            level=level,
            complete=complete,
            explainable=explainable,
            falsifiable=falsifiable,
            internally_consistent=internally_consistent,
            evidence_supported=evidence_supported,
            rationale=(
                f"Reasoning satisfied "
                f"{score} of 5 quality criteria."
            ),
        )

    # ==============================================================
    # Thesis Generation
    # ==============================================================

    def _generate_central_claim(
        self,
        context: StructuralContext,
    ) -> str:
        """
        Generate the primary reasoning claim from the current
        structural context.
        """

        if context.context == "Bullish Expansion":
            return (
                "Bullish continuation is currently the most "
                "supported structural hypothesis."
            )

        if context.context == "Bearish Expansion":
            return (
                "Bearish continuation is currently the most "
                "supported structural hypothesis."
            )

        if context.context == "Transition":
            return (
                "The market is undergoing a structural transition."
            )

        return (
            "The current market structure is indeterminate."
        )
        
    def _generate_expected_structural_evolution(
        self,
        context: StructuralContext,
    ) -> str:
        """
        Forecast the most justified structural evolution
        from the current structural context.

        This forecasts structure,
        not price.
        """

        if context.context == "Bullish Expansion":

            return (
                "Continuation of the bullish structural "
                "expansion is currently the most justified "
                "expected evolution."
            )

        if context.context == "Bearish Expansion":

            return (
                "Continuation of the bearish structural "
                "expansion is currently the most justified "
                "expected evolution."
            )

        if context.context == "Transition":

            return (
                "The market is undergoing structural transition. "
                "Additional structural confirmation is required "
                "before continuation or reversal can be justified."
            )

        return (
            "No justified structural evolution can currently "
            "be established."
        )

    # ==============================================================
    # Thesis Construction
    # ==============================================================

    def _construct_market_thesis(
        self,
        market,
        context,
        supporting_evidence,
        counter_evidence,
        evidence_assessment,
        objectives,
    ) -> MarketThesis:

        return MarketThesis(
            thesis_id=str(uuid4()),
            created_at=datetime.now(UTC),

            symbol=market.symbol,
            timeframe=market.timeframe,

            reasoning_model=self.model_name,
            theory=self.theory,
            version=self.version,

            market_regime=context.context,
            session="UNKNOWN",

            objectives=tuple(objectives or ()),

            central_claim=self._generate_central_claim(
                context
            ),

            supporting_evidence=supporting_evidence,

            counter_evidence=counter_evidence,

            assumptions=(
                "Current structural context remains valid.",
            ),

            expected_structural_evolution=(
                self._generate_expected_structural_evolution(
                    context
                )
            ),

            invalidation=(
                "Confirmed opposing CHOCH.",
            ),

            uncertainty=evidence_assessment.level,
        )