from architecture.selection.candidate import Candidate
from architecture.selection.candidate_generator import CandidateGenerator


class ICTOriginCandidateGenerator(CandidateGenerator):

    def generate(
        self,
        expansion,
        configuration
    ):

        candidates = []

        df = configuration.df

        start = expansion.base_swing_index
        end = expansion.end_index

        candidate_id = 1

        for i in range(start, end + 1):

            candle = df.iloc[i]

            # --------------------------
            # Bullish Expansion
            # Eligible = Bearish Candle
            # --------------------------
            if (
                expansion.direction == "BULLISH"
                and candle["Close"] < candle["Open"]
            ):

                candidates.append(
                    Candidate(
                        id=candidate_id,
                        subject=i,
                        metadata={}
                    )
                )

                candidate_id += 1

            # --------------------------
            # Bearish Expansion
            # Eligible = Bullish Candle
            # --------------------------
            elif (
                expansion.direction == "BEARISH"
                and candle["Close"] > candle["Open"]
            ):

                candidates.append(
                    Candidate(
                        id=candidate_id,
                        subject=i,
                        metadata={}
                    )
                )

                candidate_id += 1

        return candidates