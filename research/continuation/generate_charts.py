from pathlib import Path
from enum import Enum

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D


# ==========================================================
# Research Configuration
# ==========================================================

RESEARCH_CATEGORY = "successful"

SYMBOL = "ACUTAAS"

TIMEFRAME = "1m"


# ==========================================================
# Input / Output Paths
# ==========================================================

INPUT_HISTORY = Path(
    f"historical_data/normalized/{SYMBOL}_{TIMEFRAME}.csv"
)

INPUT_REVIEW_SAMPLE = Path(
    f"research/continuation/{RESEARCH_CATEGORY}/review_sample.csv"
)

OUTPUT_DIR = Path(
    f"research/continuation/{RESEARCH_CATEGORY}/charts"
)
# ==========================================================
# Chart Mode
# ==========================================================

class ChartMode(Enum):

    CLEAN = "clean"

    ANNOTATED = "annotated"
# ==========================================================
# Research Window
# ==========================================================

WINDOW_SIZE = 180

WINDOW_BEFORE_RATIO = 0.75
WINDOW_AFTER_RATIO = 0.25

WINDOW_BEFORE = int(
    WINDOW_SIZE * WINDOW_BEFORE_RATIO
)

WINDOW_AFTER = WINDOW_SIZE - WINDOW_BEFORE

FIGURE_WIDTH = 16
FIGURE_HEIGHT = 8


# ==========================================================
# Data Loading
# ==========================================================

def load_history():

    df = pd.read_csv(INPUT_HISTORY)

    required_columns = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Missing columns: {missing}"
        )

    return df


def load_review_sample():

    review_sample = pd.read_csv(
        INPUT_REVIEW_SAMPLE
    )

def load_review_sample():

    if not INPUT_REVIEW_SAMPLE.exists():

        raise FileNotFoundError(

            f"Review sample not found:\n"
            f"{INPUT_REVIEW_SAMPLE}"

        )

    return pd.read_csv(
        INPUT_REVIEW_SAMPLE
    )


# ==========================================================
# Window Extraction
# ==========================================================

def extract_window(
    history_df,
    continuation_index,
):
    """
    Extract a research window around the continuation.

    The continuation event is intentionally shifted
    toward the right so more historical context is
    visible.
    """

    start = max(
        0,
        continuation_index - WINDOW_BEFORE,
    )

    end = min(
        len(history_df),
        continuation_index + WINDOW_AFTER + 1,
    )

    window = (
        history_df
        .iloc[start:end]
        .copy()
        .reset_index(drop=True)
    )

    return (
        window,
        start,
        end,
    )

# ==========================================================
# Output Helpers
# ==========================================================

def prepare_output_directory():

    (OUTPUT_DIR / "clean").mkdir(
        parents=True,
        exist_ok=True,
    )

    (OUTPUT_DIR / "annotated").mkdir(
        parents=True,
        exist_ok=True,
    )


def output_path(
    example_id,
    mode,
):

    folder = (
        OUTPUT_DIR
        / mode.value
    )

    return (
        folder
        /
        f"{example_id}.png"
    )
# ==========================================================
# Candlestick Renderer
# ==========================================================

UP_CANDLE_COLOR = "#2ecc71"
DOWN_CANDLE_COLOR = "#e74c3c"
WICK_COLOR = "black"

BODY_WIDTH = 0.60
WICK_WIDTH = 1.0


def draw_candlestick(
    ax,
    x,
    open_price,
    high_price,
    low_price,
    close_price,
):
    """
    Draws a single candlestick.
    """

    bullish = close_price >= open_price

    color = (
        UP_CANDLE_COLOR
        if bullish
        else DOWN_CANDLE_COLOR
    )

    # -----------------------------
    # Wick
    # -----------------------------

    ax.vlines(
        x,
        low_price,
        high_price,
        color=WICK_COLOR,
        linewidth=WICK_WIDTH,
        zorder=1,
    )

    # -----------------------------
    # Candle Body
    # -----------------------------

    body_bottom = min(
        open_price,
        close_price,
    )

    body_height = abs(
        close_price - open_price
    )

    # Doji
    if body_height == 0:
        body_height = 0.01

    rectangle = plt.Rectangle(

        (
            x - BODY_WIDTH / 2,
            body_bottom,
        ),

        BODY_WIDTH,

        body_height,

        facecolor=color,

        edgecolor=color,

        linewidth=1,

        zorder=2,

    )

    ax.add_patch(rectangle)

# ==========================================================
# Chart Drawing
# ==========================================================

def draw_chart(
    window_df,
    output_file,
    example,
    window_start,
    mode=ChartMode.ANNOTATED,
):

    fig, ax = plt.subplots(

        figsize=(
            FIGURE_WIDTH,
            FIGURE_HEIGHT,
        )

    )

    # ----------------------------------------
    # Draw every candle
    # ----------------------------------------

    for x, candle in enumerate(
        window_df.itertuples()
    ):

        draw_candlestick(

            ax=ax,

            x=x,

            open_price=candle.open,

            high_price=candle.high,

            low_price=candle.low,

            close_price=candle.close,

        )

    # ----------------------------------------
    # Formatting
    # ----------------------------------------

    if mode == ChartMode.ANNOTATED:
        draw_chart_header(
            ax,
            example,
        )

        draw_chart_legend(
            ax,
        )

    ax.set_xlabel(
        f"Window "
        f"(-{WINDOW_BEFORE} ... "
        f"+{WINDOW_AFTER})",
        fontsize=11,
    )

    ax.set_ylabel(
        "Price",
        fontsize=11,
    )

    ax.grid(
        which="major",
        linestyle="--",
        linewidth=0.5,
        alpha=0.35,
    )

    ax.set_xlim(
        -1,
        len(window_df),
    )

    ymin = window_df["low"].min()

    ymax = window_df["high"].max()

    padding = (
        ymax - ymin
    ) * 0.05
    chart_top = ymax + padding
    ax.set_ylim(

        ymin - padding,

        ymax + padding,

    )
    if mode == ChartMode.ANNOTATED:

        highlight_pullback(
            ax=ax,
            example=example,
            window_start=window_start,
            window_length=len(window_df),
        )

        highlight_future(
            ax=ax,
            example=example,
            window_start=window_start,
            window_length=len(window_df),
        )

        draw_event_markers(
            ax=ax,
            example=example,
            window_start=window_start,
            window_length=len(window_df),
            ymax=chart_top,
        )
    plt.xticks(
        rotation=45,
    )
    plt.tight_layout()

    plt.savefig(

        output_file,

        dpi=150,

        bbox_inches="tight",

    )

    plt.close(fig)
# ==========================================================
# Annotation Configuration
# ==========================================================

IMPULSE_START_COLOR = "green"
IMPULSE_END_COLOR = "blue"
PULLBACK_END_COLOR = "orange"
CONTINUATION_COLOR = "red"

ANNOTATION_LINESTYLE = "--"
ANNOTATION_LINEWIDTH = 1.2

CONTINUATION_LINEWIDTH = 2.5
# ==========================================================
# Helper
# ==========================================================

def _draw_vertical_marker(
    ax,
    x,
    label,
    color,
    linewidth,
    ymax,
):
    """
    Draw a vertical research marker.

    Parameters
    ----------
    ax : matplotlib axis

    x : int
        Candle position inside the extracted window.

    label : str

    color : str

    linewidth : float

    ymax : float
        Top of the current chart.
    """

    ax.axvline(
        x=x,
        color=color,
        linestyle=ANNOTATION_LINESTYLE,
        linewidth=linewidth,
        alpha=0.90,
        zorder=10,
    )

    ax.text(
        x,
        ymax,
        label,
        rotation=90,
        color=color,
        fontsize=9,
        fontweight="bold",
        ha="center",
        va="bottom",
    )
    ax.text(

        0.01,

        0.98,

        "Research Question:\n"
        "What objective event occurred\n"
        "before continuation?",

        transform=ax.transAxes,

        fontsize=9,

        verticalalignment="top",

        bbox=dict(
            facecolor="white",
            alpha=0.85,
        ),

    )
    ax.text(

        0.99,

        0.01,

        "Research Viewer v1",

        transform=ax.transAxes,

        fontsize=8,

        ha="right",

        alpha=0.45,

    )

# ==========================================================
# Event Marker Overlay
# ==========================================================

def draw_event_markers(
    ax,
    example,
    window_start,
    window_length,
    ymax,
):
    """
    Draws research annotations.

    Window coordinates:

    absolute candle index
            ↓
    chart coordinate
    """

    markers = [

        (
            "IS",
            int(example.impulse_start),
            IMPULSE_START_COLOR,
            ANNOTATION_LINEWIDTH,
        ),

        (
            "IE",
            int(example.impulse_end),
            IMPULSE_END_COLOR,
            ANNOTATION_LINEWIDTH,
        ),

        (
            "PB",
            int(example.pullback_end),
            PULLBACK_END_COLOR,
            ANNOTATION_LINEWIDTH,
        ),

        (
            "CONT",
            int(example.continuation_index),
            CONTINUATION_COLOR,
            CONTINUATION_LINEWIDTH,
        ),

    ]

    for (
        label,
        absolute_index,
        color,
        width,
    ) in markers:

        x = absolute_index - window_start

        # Ignore markers outside the chart
        if x < 0:
            continue

        if x >= window_length:
            continue

        _draw_vertical_marker(
            ax=ax,
            x=x,
            label=label,
            color=color,
            linewidth=width,
            ymax=ymax,
        )
# ==========================================================
# Pullback Highlight
# ==========================================================

def highlight_pullback(
    ax,
    example,
    window_start,
    window_length,
):

    impulse_end = (
        int(example.impulse_end)
        - window_start
    )

    pullback_end = (
        int(example.pullback_end)
        - window_start
    )

    if (
        impulse_end < 0
        or
        pullback_end >= window_length
        or
        impulse_end >= pullback_end
    ):
        return

    ax.axvspan(
        impulse_end,
        pullback_end,
        color="gold",
        alpha=0.10,
        zorder=0,
    )
# ==========================================================
# Future Highlight
# ==========================================================

def highlight_future(
    ax,
    example,
    window_start,
    window_length,
):

    continuation = (
        int(example.continuation_index)
        - window_start
    )

    if (
        continuation < 0
        or
        continuation >= window_length
    ):
        return

    ax.axvspan(
        continuation,
        window_length,
        color="lightgray",
        alpha=0.15,
        zorder=0,
    )
# ==========================================================
# Chart Header
# ==========================================================

def draw_chart_header(
    ax,
    example,
):

    title = (
    f"{example.Example_ID} | {example.direction}\n"
    f"Impulse {example.impulse_size:.2f}%"
    f"   "
    f"Retrace {example.retracement_percent:.2f}%\n"
    f"Window {WINDOW_BEFORE}/{WINDOW_AFTER}"
)
    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold",
        pad=20,
    )



# ==========================================================
# Legend
# ==========================================================

def draw_chart_legend(ax):

    handles = [

        Line2D(
            [0],
            [0],
            color=IMPULSE_START_COLOR,
            linestyle="--",
            linewidth=2,
            label="Impulse Start",
        ),

        Line2D(
            [0],
            [0],
            color=IMPULSE_END_COLOR,
            linestyle="--",
            linewidth=2,
            label="Impulse End",
        ),

        Line2D(
            [0],
            [0],
            color=PULLBACK_END_COLOR,
            linestyle="--",
            linewidth=2,
            label="Pullback End",
        ),

        Line2D(
            [0],
            [0],
            color=CONTINUATION_COLOR,
            linestyle="--",
            linewidth=3,
            label="Continuation",
        ),

    ]

    ax.legend(
        handles=handles,
        loc="upper left",
        fontsize=9,
    )
# ==========================================================
# Main
# ==========================================================

# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("RESEARCH CHART GENERATOR")
    print("=" * 60)

    print(
        f"Research Category : {RESEARCH_CATEGORY}"
    )

    print(
        f"Symbol            : {SYMBOL}"
    )

    print(
        f"Timeframe         : {TIMEFRAME}"
    )

    print(
        f"Research Window   : "
        f"{WINDOW_BEFORE} before / "
        f"{WINDOW_AFTER} after"
    )

    print()

    prepare_output_directory()

    history = load_history()

    review_examples = load_review_sample()

    total = len(review_examples)

    print(
        f"History Candles   : {len(history):,}"
    )

    print(
        f"Review Sample     : {total}"
    )

    print()

    for i, example in enumerate(
        review_examples.itertuples(index=False),
        start=1,
    ):

        example_id = example.Example_ID

        continuation_index = int(
            example.continuation_index
        )

        window_df, start, end = extract_window(
            history,
            continuation_index,
        )

        for mode in (

            ChartMode.CLEAN,

            ChartMode.ANNOTATED,

        ):

            save_path = output_path(
                example_id,
                mode,
            )

            draw_chart(

                window_df=window_df,

                output_file=save_path,

                example=example,

                window_start=start,

                mode=mode,

            )

        print(
            f"[{i:03d}/{total:03d}] "
            f"{example_id}"
        )

    charts_created = total * 2

    print()
    print("=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)

    print(
        f"Examples          : {total}"
    )

    print(
        f"Clean Charts      : {total}"
    )

    print(
        f"Annotated Charts  : {total}"
    )

    print(
        f"Total PNGs        : {charts_created}"
    )

    print(
        f"Output Folder     : {OUTPUT_DIR}"
    )

    print()

    print("Research Dataset Ready ✓")


if __name__ == "__main__":
    main()