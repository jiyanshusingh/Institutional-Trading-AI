from engines.indicator_engine import IndicatorEngine
from engines.swing_engine import SwingEngine
from engines.market_structure import MarketStructure
from engines.smc_engine import SMCEngine
from engines.structure_event_engine import StructureEventEngine
from engines.segment_engine import SegmentEngine
from engines.expansion_engine import ExpansionEngine

class MarketAnalysisEngine:

    def __init__(self):

        # Structure

        self.swing_engine = ...

        self.structure_engine = ...

        self.segment_engine = ...

        self.expansion_engine = ...

        # Regions

        self.origin_region_engine = ...

        self.order_block_engine = ...

        self.fvg_engine = ...

        self.liquidity_engine = ...

        # Relationships

        self.relationship_engine = ...

    def analyze(self, df):
        # Stage 0
        indicator_engine = IndicatorEngine()
        df = indicator_engine.calculate(df)

        # Stage 1
        swing_engine = SwingEngine(df)
        df = swing_engine.detect()
        
        # Stage 2
        market_structure = MarketStructure(df)
        df = market_structure.classify_structure()
        df = market_structure.detect_trend_candidate()
        df = market_structure.detect_protected_swings()
        df = market_structure.detect_bos()
        df = market_structure.detect_choch()
        
        # Market State
        market_structure = MarketStructure(df)
        df = market_structure.detect_market_state()

        # Stage 2
        structure_engine = StructureEventEngine(df)
        structure_events = structure_engine.generate_events()

        # Stage 3
        segment_engine = SegmentEngine(structure_events)
        segments = segment_engine.build()

        # Stage 4
        expansion_engine = ExpansionEngine(
            segments,
            structure_events
        )
        expansions = expansion_engine.build()

        # TODO
        # Origin Regions

        # TODO
        # Order Blocks

        # TODO
        # Fair Value Gaps

        # TODO
        # Liquidity Regions

        # TODO
        # Relationships

        # TODO
        # Market Configuration

        return expansions