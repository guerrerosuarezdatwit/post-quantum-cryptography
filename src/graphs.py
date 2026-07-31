"""
Generate comparative benchmark plots for all registered algorithms.

Timing statistics are loaded from combined_summary.csv. Key, ciphertext,
and shared-secret sizes are loaded from each algorithm's raw-results CSV.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


RESULTS_DIRECTORY = Path("results")
PLOTS_DIRECTORY = RESULTS_DIRECTORY / "plots"
COMBINED_SUMMARY_PATH = RESULTS_DIRECTORY / "combined_summary.csv"

RAW_RESULTS_PATTERN = "*_raw_results.csv"

METRIC_DISPLAY_NAMES = {
    "key_generation_ms": "Key Generation",
    "encapsulation_ms": "Forward Operation",
    "decapsulation_ms": "Reverse Operation",
    "exchange_ms": "Total Exchange",
}

SIZE_DISPLAY_NAMES = {
    "public_key_size": "Public Key",
    "private_key_size": "Private Key",
    "ciphertext_size": "Ciphertext",
    "shared_secret_size": "Shared Secret",
}


def validate_input_files() -> list[Path]:
    """Confirm that the benchmark CSV files exist."""

    if not COMBINED_SUMMARY_PATH.exists():
        raise FileNotFoundError(
            f"Missing benchmark summary: {COMBINED_SUMMARY_PATH}\n"
            "Run `python src/benchmark.py` before generating graphs."
        )

    raw_result_paths = sorted(
        RESULTS_DIRECTORY.glob(RAW_RESULTS_PATTERN)
    )

    if not raw_result_paths:
        raise FileNotFoundError(
            "No raw benchmark CSV files were found.\n"
            "Run `python src/benchmark.py` before generating graphs."
        )

    return raw_result_paths


def load_timing_summary() -> pd.DataFrame:
    """Load and validate the combined timing summary."""

    summary = pd.read_csv(COMBINED_SUMMARY_PATH)

    required_columns = {
        "algorithm",
        "metric",
        "mean_ms",
        "median_ms",
        "stddev_ms",
        "minimum_ms",
        "maximum_ms",
    }

    missing_columns = required_columns - set(summary.columns)

    if missing_columns:
        formatted_columns = ", ".join(sorted(missing_columns))

        raise ValueError(
            "combined_summary.csv is missing required columns: "
            f"{formatted_columns}"
        )

    return summary


def load_size_summary(raw_result_paths: list[Path]) -> pd.DataFrame:
    """
    Load one representative size record for each algorithm.

    Key and ciphertext sizes remain constant across benchmark iterations,
    so only the first row from each raw-results file is needed.
    """

    size_records: list[dict[str, str | int]] = []

    required_columns = {
        "algorithm",
        "public_key_size",
        "private_key_size",
        "ciphertext_size",
        "shared_secret_size",
    }

    for path in raw_result_paths:
        raw_results = pd.read_csv(path, nrows=1)

        missing_columns = required_columns - set(raw_results.columns)

        if missing_columns:
            formatted_columns = ", ".join(sorted(missing_columns))

            raise ValueError(
                f"{path} is missing required columns: "
                f"{formatted_columns}"
            )

        first_row = raw_results.iloc[0]

        size_records.append(
            {
                "algorithm": str(first_row["algorithm"]),
                "public_key_size": int(first_row["public_key_size"]),
                "private_key_size": int(first_row["private_key_size"]),
                "ciphertext_size": int(first_row["ciphertext_size"]),
                "shared_secret_size": int(
                    first_row["shared_secret_size"]
                ),
            }
        )

    return pd.DataFrame(size_records).drop_duplicates(
        subset="algorithm"
    )


def save_plot(filename: str) -> None:
    """Save the current figure and close it."""

    output_path = PLOTS_DIRECTORY / filename

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Created {output_path}")


def plot_key_generation_comparison(
    summary: pd.DataFrame,
) -> None:
    """Compare mean key-generation time across algorithms."""

    data = summary[
        summary["metric"] == "key_generation_ms"
    ].copy()

    data = data.sort_values("mean_ms")

    plt.figure(figsize=(9, 6))
    plt.bar(
        data["algorithm"],
        data["mean_ms"],
        yerr=data["stddev_ms"],
        capsize=5,
    )

    plt.title("Mean Key Generation Time")
    plt.xlabel("Algorithm")
    plt.ylabel("Time (ms)")
    plt.grid(axis="y", alpha=0.3)

    save_plot("key_generation_comparison.png")


def plot_key_generation_log_scale(
    summary: pd.DataFrame,
) -> None:
    """
    Compare key-generation times using a logarithmic scale.

    This makes ECDH and ML-KEM visible despite RSA's much larger time.
    """

    data = summary[
        summary["metric"] == "key_generation_ms"
    ].copy()

    data = data.sort_values("mean_ms")

    plt.figure(figsize=(9, 6))
    plt.bar(
        data["algorithm"],
        data["mean_ms"],
        yerr=data["stddev_ms"],
        capsize=5,
    )

    plt.yscale("log")
    plt.title("Mean Key Generation Time — Log Scale")
    plt.xlabel("Algorithm")
    plt.ylabel("Time (ms, logarithmic scale)")
    plt.grid(axis="y", alpha=0.3)

    save_plot("key_generation_comparison_log.png")


def plot_exchange_time_comparison(
    summary: pd.DataFrame,
) -> None:
    """Compare mean total exchange time across algorithms."""

    data = summary[
        summary["metric"] == "exchange_ms"
    ].copy()

    data = data.sort_values("mean_ms")

    plt.figure(figsize=(9, 6))
    plt.bar(
        data["algorithm"],
        data["mean_ms"],
        yerr=data["stddev_ms"],
        capsize=5,
    )

    plt.title("Mean Total Exchange Time")
    plt.xlabel("Algorithm")
    plt.ylabel("Time (ms)")
    plt.grid(axis="y", alpha=0.3)

    save_plot("exchange_time_comparison.png")


def plot_operation_comparison(
    summary: pd.DataFrame,
) -> None:
    """Create a grouped comparison of all measured operations."""

    data = summary[
        summary["metric"].isin(METRIC_DISPLAY_NAMES)
    ].copy()

    data["operation"] = data["metric"].map(
        METRIC_DISPLAY_NAMES
    )

    pivot_table = data.pivot(
        index="algorithm",
        columns="operation",
        values="mean_ms",
    )

    ordered_columns = [
        display_name
        for metric, display_name in METRIC_DISPLAY_NAMES.items()
        if display_name in pivot_table.columns
    ]

    pivot_table = pivot_table[ordered_columns]

    axis = pivot_table.plot(
        kind="bar",
        figsize=(11, 7),
    )

    axis.set_title("Mean Operation Time by Algorithm")
    axis.set_xlabel("Algorithm")
    axis.set_ylabel("Time (ms)")
    axis.tick_params(axis="x", rotation=0)
    axis.grid(axis="y", alpha=0.3)
    axis.legend(title="Operation")

    save_plot("operation_time_comparison.png")


def plot_key_size_comparison(
    sizes: pd.DataFrame,
) -> None:
    """Compare serialized public- and private-key sizes."""

    data = sizes.set_index("algorithm")[
        [
            "public_key_size",
            "private_key_size",
        ]
    ].rename(
        columns={
            "public_key_size": SIZE_DISPLAY_NAMES[
                "public_key_size"
            ],
            "private_key_size": SIZE_DISPLAY_NAMES[
                "private_key_size"
            ],
        }
    )

    axis = data.plot(
        kind="bar",
        figsize=(10, 7),
    )

    axis.set_title("Serialized Key Size Comparison")
    axis.set_xlabel("Algorithm")
    axis.set_ylabel("Size (bytes)")
    axis.tick_params(axis="x", rotation=0)
    axis.grid(axis="y", alpha=0.3)
    axis.legend(title="Key Type")

    save_plot("key_size_comparison.png")


def plot_output_size_comparison(
    sizes: pd.DataFrame,
) -> None:
    """Compare ciphertext and shared-secret sizes."""

    data = sizes.set_index("algorithm")[
        [
            "ciphertext_size",
            "shared_secret_size",
        ]
    ].rename(
        columns={
            "ciphertext_size": SIZE_DISPLAY_NAMES[
                "ciphertext_size"
            ],
            "shared_secret_size": SIZE_DISPLAY_NAMES[
                "shared_secret_size"
            ],
        }
    )

    axis = data.plot(
        kind="bar",
        figsize=(10, 7),
    )

    axis.set_title("Ciphertext and Shared-Secret Size Comparison")
    axis.set_xlabel("Algorithm")
    axis.set_ylabel("Size (bytes)")
    axis.tick_params(axis="x", rotation=0)
    axis.grid(axis="y", alpha=0.3)
    axis.legend(title="Data Type")

    save_plot("output_size_comparison.png")


def main() -> None:
    """Generate all comparative benchmark plots."""

    raw_result_paths = validate_input_files()

    PLOTS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    timing_summary = load_timing_summary()
    size_summary = load_size_summary(raw_result_paths)

    plot_key_generation_comparison(timing_summary)
    plot_key_generation_log_scale(timing_summary)
    plot_exchange_time_comparison(timing_summary)
    plot_operation_comparison(timing_summary)
    plot_key_size_comparison(size_summary)
    plot_output_size_comparison(size_summary)

    print("\nAll comparative graphs generated successfully.")


if __name__ == "__main__":
    main()