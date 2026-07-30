from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


RESULTS_DIRECTORY = Path("results")
PLOTS_DIRECTORY = RESULTS_DIRECTORY / "plots"

RAW_RESULTS_PATH = RESULTS_DIRECTORY / "mlkem_raw_results.csv"
SUMMARY_PATH = RESULTS_DIRECTORY / "mlkem_summary.csv"


DISPLAY_NAMES = {
    "key_generation_ms": "Key Generation",
    "encapsulation_ms": "Encapsulation",
    "decapsulation_ms": "Decapsulation",
    "exchange_ms": "Total Exchange",
}


def validate_input_files() -> None:
    """Confirm that the benchmark CSV files exist."""

    missing_files = [
        path
        for path in (RAW_RESULTS_PATH, SUMMARY_PATH)
        if not path.exists()
    ]

    if missing_files:
        formatted_paths = "\n".join(f"  - {path}" for path in missing_files)

        raise FileNotFoundError(
            "The following benchmark files are missing:\n"
            f"{formatted_paths}\n"
            "Run `python src/benchmark.py` before generating graphs."
        )


def load_results() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load raw and summarized benchmark results."""

    validate_input_files()

    raw_results = pd.read_csv(RAW_RESULTS_PATH)
    summary = pd.read_csv(SUMMARY_PATH)

    return raw_results, summary


def save_figure(filename: str) -> None:
    """Save the active Matplotlib figure and close it."""

    PLOTS_DIRECTORY.mkdir(parents=True, exist_ok=True)

    output_path = PLOTS_DIRECTORY / filename

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Created {output_path}")


def create_operation_comparison(summary: pd.DataFrame) -> None:
    """
    Create a bar chart comparing the mean duration of each ML-KEM stage.

    Error bars represent one standard deviation.
    """

    timing_summary = summary[
        summary["metric"].isin(DISPLAY_NAMES)
    ].copy()

    timing_summary["display_name"] = timing_summary["metric"].map(
        DISPLAY_NAMES
    )

    plt.figure(figsize=(9, 5))

    plt.bar(
        timing_summary["display_name"],
        timing_summary["mean_ms"],
        yerr=timing_summary["stddev_ms"],
        capsize=5,
    )

    plt.title("ML-KEM-768 Mean Execution Time by Operation")
    plt.xlabel("Operation")
    plt.ylabel("Time (milliseconds)")
    plt.grid(axis="y", alpha=0.3)

    save_figure("mlkem_operation_comparison.png")


def create_exchange_histogram(raw_results: pd.DataFrame) -> None:
    """Create a histogram of total ML-KEM exchange times."""

    plt.figure(figsize=(9, 5))

    plt.hist(
        raw_results["exchange_ms"],
        bins=40,
        edgecolor="black",
    )

    mean_exchange = raw_results["exchange_ms"].mean()
    median_exchange = raw_results["exchange_ms"].median()

    plt.axvline(
        mean_exchange,
        linestyle="--",
        label=f"Mean: {mean_exchange:.4f} ms",
    )

    plt.axvline(
        median_exchange,
        linestyle=":",
        label=f"Median: {median_exchange:.4f} ms",
    )

    plt.title("Distribution of ML-KEM-768 Exchange Times")
    plt.xlabel("Total exchange time (milliseconds)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

    save_figure("mlkem_exchange_distribution.png")


def create_exchange_over_iterations(raw_results: pd.DataFrame) -> None:
    """Plot total exchange time across all measured iterations."""

    plt.figure(figsize=(10, 5))

    plt.plot(
        raw_results["iteration"],
        raw_results["exchange_ms"],
        linewidth=0.8,
    )

    mean_exchange = raw_results["exchange_ms"].mean()

    plt.axhline(
        mean_exchange,
        linestyle="--",
        label=f"Mean: {mean_exchange:.4f} ms",
    )

    plt.title("ML-KEM-768 Exchange Time Across 1,000 Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Total exchange time (milliseconds)")
    plt.legend()
    plt.grid(alpha=0.3)

    save_figure("mlkem_exchange_over_iterations.png")


def main() -> None:
    raw_results, summary = load_results()

    create_operation_comparison(summary)
    create_exchange_histogram(raw_results)
    create_exchange_over_iterations(raw_results)

    print("\nAll graphs generated successfully.")


if __name__ == "__main__":
    main()