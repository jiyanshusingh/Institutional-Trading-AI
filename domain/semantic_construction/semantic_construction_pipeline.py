"""
Semantic Construction Pipeline

Transforms an ObservationHistory into a
CanonicalMarketModel.
"""

from domain.market_observation.observation_history import ObservationHistory

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

# ---------------------------------------------------------
# Swing
# ---------------------------------------------------------

from domain.ontology.builders.swing_builder import SwingBuilder

from domain.ontology.candidates.ict.ict_swing_candidate_detector import (
    ICTSwingCandidateDetector,
)

from domain.ontology.policies.ict.ict_swing_confirmation_policy import (
    ICTSwingConfirmationPolicy,
)

from domain.ontology.calculations.swing_strength_calculator import (
    SwingStrengthCalculator,
)

# ---------------------------------------------------------
# Structure Event
# ---------------------------------------------------------

from domain.ontology.builders.structure_event_builder import (
    StructureEventBuilder,
)

from domain.ontology.candidates.ict.ict_structure_event_candidate_detector import (
    ICTStructureEventCandidateDetector,
)

from domain.ontology.policies.ict.ict_structure_event_confirmation_policy import (
    ICTStructureEventConfirmationPolicy,
)
from domain.ontology.builders.protected_swing_builder import (
    ProtectedSwingBuilder,
)

from domain.ontology.candidates.ict.ict_protected_swing_candidate_detector import (
    ICTProtectedSwingCandidateDetector,
)

from domain.ontology.policies.ict.ict_protected_swing_confirmation_policy import (
    ICTProtectedSwingConfirmationPolicy,
)

from domain.ontology.builders.expansion_builder import (
    ExpansionBuilder,
)

from domain.ontology.candidates.ict.ict_expansion_candidate_detector import (
    ICTExpansionCandidateDetector,
)

from domain.ontology.policies.ict.ict_expansion_confirmation_policy import (
    ICTExpansionConfirmationPolicy,
)

from domain.ontology.builders.origin_region_builder import (
    OriginRegionBuilder,
)

from domain.ontology.candidates.ict.ict_origin_region_candidate_detector import (
    ICTOriginRegionCandidateDetector,
)

from domain.ontology.policies.ict.ict_origin_region_confirmation_policy import (
    ICTOriginRegionConfirmationPolicy,
)
from domain.ontology.builders.fair_value_gap_builder import (
    FairValueGapBuilder,
)

from domain.ontology.candidates.ict.ict_fair_value_gap_candidate_detector import (
    ICTFairValueGapCandidateDetector,
)

from domain.ontology.policies.ict.ict_fair_value_gap_confirmation_policy import (
    ICTFairValueGapConfirmationPolicy,
)

class SemanticConstructionPipeline:

    def __init__(self):
        # ---------------------------------------------
        # Swing Builder
        # ---------------------------------------------
        self._swing_builder = SwingBuilder(

            detector=ICTSwingCandidateDetector(
                lookback=1,
            ),

            confirmation_policy=ICTSwingConfirmationPolicy(

                strength_calculator=SwingStrengthCalculator(),

                lookback=1,
            ),
        )
        # ---------------------------------------------
        # Structure Event Builder
        # ---------------------------------------------
        self._structure_event_builder = StructureEventBuilder(

            detector=ICTStructureEventCandidateDetector(),

            confirmation_policy=ICTStructureEventConfirmationPolicy(),

        )      
        # ---------------------------------------------
        # Protected Swing Builder
        # ---------------------------------------------
        self._protected_swing_builder = ProtectedSwingBuilder(

            detector=ICTProtectedSwingCandidateDetector(),

            confirmation_policy=ICTProtectedSwingConfirmationPolicy(),

        )
        
        self._expansion_builder = ExpansionBuilder(

            detector=ICTExpansionCandidateDetector(),

            confirmation_policy=ICTExpansionConfirmationPolicy(),

        )
        
        self._origin_region_builder = OriginRegionBuilder(

            detector=ICTOriginRegionCandidateDetector(),

            confirmation_policy=ICTOriginRegionConfirmationPolicy(),

        )
        
        self._fair_value_gap_builder = FairValueGapBuilder(

            detector=ICTFairValueGapCandidateDetector(),

            confirmation_policy=ICTFairValueGapConfirmationPolicy(),

        )
    

    def build(
            self,
            observation_history: ObservationHistory,
        ) -> CanonicalMarketModel:

            #
            # Stage 1
            # Swings
            #

            swings = self._swing_builder.build(
                observation_history,
            )

            #
            # Stage 2
            # Structure Events
            #

            structure_events = (
                self._structure_event_builder.build(
                    observation_history,
                    swings=swings,
                )
            )

            #
            # Intermediate semantic model
            #

            intermediate_model = CanonicalMarketModel(

                observation_history=observation_history,

                swings=swings,

                structure_events=structure_events,

            )

            #
            # Stage 3
            # Protected Swings
            #

            protected_swings = (
                self._protected_swing_builder.build(
                    intermediate_model,
                )
            )
            
            protected_model = CanonicalMarketModel(

                observation_history=observation_history,

                swings=swings,

                structure_events=structure_events,

                protected_swings=protected_swings,

            )
            
            expansions = self._expansion_builder.build(
                protected_model,
            )
            
            expansion_model = CanonicalMarketModel(

                observation_history=observation_history,

                swings=swings,

                structure_events=structure_events,

                protected_swings=protected_swings,

                expansions=expansions,

            )
            
            origin_regions = (
                self._origin_region_builder.build(
                    expansion_model,
                )
            )
            
            origin_region_model = CanonicalMarketModel(

                observation_history=observation_history,

                swings=swings,

                structure_events=structure_events,

                protected_swings=protected_swings,

                expansions=expansions,

                origin_regions=origin_regions,

            )
            
            fair_value_gaps = (
                self._fair_value_gap_builder.build(
                    origin_region_model,
                )
            )

            #
            # Final canonical model
            #

            return CanonicalMarketModel(
                observation_history=observation_history,
                swings=swings,
                structure_events=structure_events,
                protected_swings=protected_swings,
                expansions=expansions,
                origin_regions=origin_regions,
                fair_value_gaps=fair_value_gaps,


            )