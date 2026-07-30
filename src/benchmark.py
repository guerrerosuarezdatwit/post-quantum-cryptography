import csv
from pathlib import Path
from statistics import mean, median, stdev
from typing import Any
from validation import validate_benchmark_result

from algorithms import (
    AlgorithmFunction,
    BenchmarkResult,
    get_algorithms,
)

from config import (
    BENCHMARK_ITERATIONS,
    RESULTS_DIRECTORY,
    WARMUP_ITERATIONS,
)

TIMING_FIELDS = (
    "key_generation_ms",
    "encapsulation_ms",
    "decapsulation_ms",
    "exchange_ms",
)

SIZE_FIELDS = (
    "public_key_size",
    "private_key_size",
    "ciphertext_size",
    "shared_secret_size",
)


def create_safe_filename(algorithm_name: str) -> str:
    """Convert an algorithm name into a safe lowercase filename."""

    return (
        algorithm_name.lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def benchmark_algorithm(
    algorithm_function: AlgorithmFunction,
    runs: int,
    warmup_runs: int,
) -> tuple[list[BenchmarkResult], list[dict[str, Any]]]:
    """Execute one cryptographic algorithm repeatedly."""

    if runs < 2:
        raise ValueError("runs must be at least 2")

    if warmup_runs < 0:
        raise ValueError("warmup_runs cannot be negative")

    initial_result = algorithm_function()
    validate_benchmark_result(initial_result)
    algorithm_name = str(initial_result["algorithm"])

    if not initial_result["success"]:
        raise RuntimeError(
            f"{algorithm_name} failed during initial validation."
        )

    print(f"\n=== Benchmarking {algorithm_name} ===")
    print(f"Running {warmup_runs} warm-up iterations...")

    for iteration in range(1, warmup_runs + 1):
        result = algorithm_function()

        if not result["success"]:
            raise RuntimeError(
                f"{algorithm_name} failed during warm-up "
                f"iteration {iteration}."
            )

    print(f"Running {runs} measured iterations...")

    raw_results: list[BenchmarkResult] = []

    for iteration in range(1, runs + 1):
        result = algorithm_function()

        if not result["success"]:
            raise RuntimeError(
                f"{algorithm_name} failed during measured "
                f"iteration {iteration}."
            )

        result["iteration"] = iteration
        raw_results.append(result)

        if iteration % 100 == 0 or iteration == runs:
            print(f"Completed {iteration}/{runs}")

    timing_fields = [
        field
        for field in TIMING_FIELDS
        if field in raw_results[0]
    ]

    summary: list[dict[str, Any]] = []

    for field in timing_fields:
        values = [float(result[field]) for result in raw_results]

        summary.append(
            {
                "algorithm": algorithm_name,
                "metric": field,
                "runs": runs,
                "mean_ms": mean(values),
                "median_ms": median(values),
                "stddev_ms": stdev(values),
                "minimum_ms": min(values),
                "maximum_ms": max(values),
            }
        )

    return raw_results, summary


def save_csv(
    rows: list[dict[str, Any]],
    output_path: Path,
) -> None:
    """Save dictionaries to a CSV file."""

    if not rows:
        raise ValueError("Cannot save an empty results list.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames: list[str] = []

    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def print_summary(
    summary: list[dict[str, Any]],
    first_result: BenchmarkResult,
) -> None:
    """Print statistical and size information."""

    algorithm_name = first_result["algorithm"]

    print(f"\n=== {algorithm_name} Summary ===")

    for row in summary:
        print(f"\n{row['metric']}")
        print(f"  Mean:               {row['mean_ms']:.4f} ms")
        print(f"  Median:             {row['median_ms']:.4f} ms")
        print(
            f"  Standard deviation: {row['stddev_ms']:.4f} ms"
        )
        print(f"  Minimum:            {row['minimum_ms']:.4f} ms")
        print(f"  Maximum:            {row['maximum_ms']:.4f} ms")

    print("\nSizes:")

    for field in SIZE_FIELDS:
        if field in first_result:
            print(f"  {field}: {first_result[field]} bytes")


def run_benchmarks(
    algorithms: list[AlgorithmFunction],
) -> None:
    """Benchmark all registered algorithm functions."""

    combined_summary: list[dict[str, Any]] = []

    for algorithm_function in algorithms:
        raw_results, summary = benchmark_algorithm(
            algorithm_function=algorithm_function,
            runs=BENCHMARK_ITERATIONS,
            warmup_runs=WARMUP_ITERATIONS,
        )

        algorithm_name = str(raw_results[0]["algorithm"])
        filename = create_safe_filename(algorithm_name)

        save_csv(
            raw_results,
            RESULTS_DIRECTORY / f"{filename}_raw_results.csv",
        )

        save_csv(
            summary,
            RESULTS_DIRECTORY / f"{filename}_summary.csv",
        )

        combined_summary.extend(summary)
        print_summary(summary, raw_results[0])

    save_csv(
        combined_summary,
        RESULTS_DIRECTORY / "combined_summary.csv",
    )

    print("\nAll benchmarks completed successfully.")
    print(
        f"Combined summary created: "
        f"{RESULTS_DIRECTORY / 'combined_summary.csv'}"
    )


def main() -> None:
    algorithms = get_algorithms()

    if not algorithms:
        raise RuntimeError(
            "No cryptographic algorithms are registered."
        )

    print(f"Registered algorithms: {len(algorithms)}")

    run_benchmarks(algorithms)


if __name__ == "__main__":
    main()