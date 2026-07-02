from models.liquidity_region import LiquidityRegion


class EqualHighLiquidityPolicy:

    def identify(self, swings, tolerance=0.10):

        if swings.empty:
            return []

        highs = sorted(swings["High"].tolist())

        regions = set()

        for i, seed in enumerate(highs):

            cluster = [seed]

            for j, price in enumerate(highs):

                if i == j:
                    continue

                candidate = cluster + [price]

                if max(candidate) - min(candidate) <= tolerance:

                    cluster.append(price)

            if len(cluster) >= 2:

                regions.add(

                    LiquidityRegion(

                        upper_price=max(cluster),

                        lower_price=min(cluster)

                    )

                )

        return sorted(
            regions,
            key=lambda region: region.lower_price
        )