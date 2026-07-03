from architecture.selection.candidate import Candidate
from architecture.selection.candidate_generator import CandidateGenerator

from models.order_block_geometry import OrderBlockGeometry


class ICTOrderBlockCandidateGenerator(CandidateGenerator):

    def generate(
        self,
        origin_region,
        configuration
    ):

        df = configuration.df

        candle = df.iloc[origin_region.start_index]

        open_price = candle["Open"]
        high_price = candle["High"]
        low_price = candle["Low"]
        close_price = candle["Close"]

        candidates = []

        # Candidate 1 - Full Candle
        full_geometry = OrderBlockGeometry(
            high_price=high_price,
            low_price=low_price
        )

        candidates.append(
            Candidate(
                id=len(candidates) + 1,
                subject=full_geometry,
                metadata={
                    "projection": "FULL_CANDLE"
                }
            )
        )

        # Candidate 2 - Candle Body
        body_geometry = OrderBlockGeometry(
            high_price=max(open_price, close_price),
            low_price=min(open_price, close_price)
        )

        candidates.append(
            Candidate(
                id=len(candidates) + 1,
                subject=body_geometry,
                metadata={
                    "projection": "BODY"
                }
            )
        )

        return tuple(candidates)