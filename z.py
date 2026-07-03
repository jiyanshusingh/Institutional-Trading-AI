import pandas as pd


class OrderBlockEngine:

    def __init__(self, df, bos_events):

        self.df = df.copy()
        self.bos_events = bos_events

        self.order_blocks = []

    # =====================================================
    # Initialize DataFrame Columns
    # =====================================================

    def initialize(self):

        self.df["Bullish_OB"] = False
        self.df["Bearish_OB"] = False

        self.df["OB_High"] = None
        self.df["OB_Low"] = None

        self.df["OB_Type"] = None
        self.df["OB_State"] = None

        self.df["OB_Source_BOS"] = None

        self.df["OB_Valid"] = False
        self.df["OB_Mitigated"] = False
        self.df["OB_Invalidated"] = False

        return self.df

    # =====================================================
    # Find Order Block Candidate
    # =====================================================

    def find_order_block_candidate(self, bos_event):

        direction = bos_event["direction"]
        bos_index = bos_event["candle_index"]

        # ----------------------------------------
        # Bullish BOS
        # ----------------------------------------

        if direction == "BULLISH":

            for j in range(bos_index - 1, -1, -1):

                open_price = self.df.iloc[j]["Open"]
                close_price = self.df.iloc[j]["Close"]

                # Last bearish candle
                if close_price < open_price:

                    return {
                        "index": j,
                        "type": "BULLISH"
                    }

        # ----------------------------------------
        # Bearish BOS
        # ----------------------------------------

        elif direction == "BEARISH":

            for j in range(bos_index - 1, -1, -1):

                open_price = self.df.iloc[j]["Open"]
                close_price = self.df.iloc[j]["Close"]

                # Last bullish candle
                if close_price > open_price:

                    return {
                        "index": j,
                        "type": "BEARISH"
                    }

        return None

    # =====================================================
    # Create Order Block Object
    # =====================================================

    def create_order_block(self, bos_event, candidate):

        if candidate is None:
            return None

        index = candidate["index"]

        order_block = {

            "ob_id": len(self.order_blocks) + 1,

            "type": candidate["type"],

            # Order Block Origin
            "origin_index": index,

            # Price Range
            "high": self.df.iloc[index]["High"],
            "low": self.df.iloc[index]["Low"],

            # Source Event
            "source_bos": bos_event["event_id"],
            "bos_index": bos_event["candle_index"],
            "bos_direction": bos_event["direction"],

            # Lifecycle
            "state": "ACTIVE",

            # Validation
            "valid": True,
            "mitigated": False,
            "invalidated": False

        }

        return order_block

    # =====================================================
    # Validate Order Block
    # =====================================================

    def validate_order_block(self, order_block):

        if order_block is None:
            return False

        # Rule 1
        if order_block["high"] <= order_block["low"]:
            return False

        # Rule 2
        if order_block["type"] not in ["BULLISH", "BEARISH"]:
            return False

        # Rule 3
        if order_block["state"] != "ACTIVE":
            return False

        return True
    def store_order_block(self, order_block):

        if order_block is None:
            return False

        self.order_blocks.append(order_block)

        return True
    def detect_order_blocks(self):

        for bos_event in self.bos_events:

            # ----------------------------------------
            # Find Candidate
            # ----------------------------------------

            candidate = self.find_order_block_candidate(
                bos_event
            )

            # ----------------------------------------
            # Create Order Block
            # ----------------------------------------

            order_block = self.create_order_block(
                bos_event,
                candidate
            )

            # ----------------------------------------
            # Validate
            # ----------------------------------------

            if self.validate_order_block(order_block):

                # ----------------------------------------
                # Store
                # ----------------------------------------

                self.store_order_block(order_block)

        return self.order_blocks
    
    def project_order_blocks(self):

        for ob in self.order_blocks:

            index = ob["origin_index"]

            # -----------------------------
            # Type
            # -----------------------------

            if ob["type"] == "BULLISH":

                self.df.at[
                    self.df.index[index],
                    "Bullish_OB"
                ] = True

            else:

                self.df.at[
                    self.df.index[index],
                    "Bearish_OB"
                ] = True

            # -----------------------------
            # Metadata
            # -----------------------------

            self.df.at[
                self.df.index[index],
                "OB_High"
            ] = ob["high"]

            self.df.at[
                self.df.index[index],
                "OB_Low"
            ] = ob["low"]

            self.df.at[
                self.df.index[index],
                "OB_Type"
            ] = ob["type"]

            self.df.at[
                self.df.index[index],
                "OB_State"
            ] = ob["state"]

            self.df.at[
                self.df.index[index],
                "OB_Source_BOS"
            ] = ob["source_bos"]

            self.df.at[
                self.df.index[index],
                "OB_Valid"
            ] = ob["valid"]

            self.df.at[
                self.df.index[index],
                "OB_Mitigated"
            ] = ob["mitigated"]

            self.df.at[
                self.df.index[index],
                "OB_Invalidated"
            ] = ob["invalidated"]

        return self.df