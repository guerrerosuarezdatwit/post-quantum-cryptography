from pathlib import Path


# Number of executions excluded before collecting measurements.
WARMUP_ITERATIONS = 50

# Number of measured executions per algorithm.
BENCHMARK_ITERATIONS = 1000

# Project output directories.
RESULTS_DIRECTORY = Path("results")
PLOTS_DIRECTORY = RESULTS_DIRECTORY / "plots"