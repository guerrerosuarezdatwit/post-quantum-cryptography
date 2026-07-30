from collections.abc import Callable
from typing import TypeAlias

from mlkem_demo import mlkem_demo


BenchmarkValue: TypeAlias = str | int | float | bool
BenchmarkResult: TypeAlias = dict[str, BenchmarkValue]
AlgorithmFunction: TypeAlias = Callable[[], BenchmarkResult]


# Central registry of algorithms available to the benchmark.
_ALGORITHMS: list[AlgorithmFunction] = [
    mlkem_demo,
]


def get_algorithms() -> list[AlgorithmFunction]:
    """
    Return all registered cryptographic implementations.

    A copy is returned so callers cannot accidentally modify
    the central registry.
    """

    return _ALGORITHMS.copy()