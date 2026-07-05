from models.fair_value_gap import FairValueGap


def main():

    fvg = FairValueGap(

        start_index=10,

        middle_index=11,

        end_index=12,

        upper_price=120.5,

        lower_price=118.2,

        direction="BULLISH",

        policy="ICT"

    )

    print()

    print("===================")
    print("FAIR VALUE GAP")
    print("===================")

    print()

    print(fvg)


if __name__ == "__main__":
    main()