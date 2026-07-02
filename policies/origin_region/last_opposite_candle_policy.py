from models.expansion import Expansion
from models.origin_region import OriginRegion
from policies.origin_region.base import OriginRegionPolicy


class LastOppositeCandlePolicy(OriginRegionPolicy):

    def identify(
        self,
        expansion: Expansion,
        df
    ) -> OriginRegion | None:

        # ------------------------------------
        # Search backwards through Expansion
        # ------------------------------------

        for i in range(
            expansion.end_index,
            expansion.start_index - 1,
            -1
        ):

            row = df.iloc[i]

            open_price = row["Open"]
            close_price = row["Close"]

            # ------------------------------------
            # Bullish Expansion
            # Last Bearish Candle
            # ------------------------------------

            if expansion.direction == "BULLISH":

                if close_price < open_price:

                    return OriginRegion(

                        start_index=i,

                        end_index=i

                    )

            # ------------------------------------
            # Bearish Expansion
            # Last Bullish Candle
            # ------------------------------------

            else:

                if close_price > open_price:

                    return OriginRegion(

                        start_index=i,

                        end_index=i

                    )

        # ------------------------------------
        # No Origin Region Found
        # ------------------------------------

        return None