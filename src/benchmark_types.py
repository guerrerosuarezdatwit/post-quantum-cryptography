from collections.abc import Callable
from typing import TypeAlias

BenchmarkValue: TypeAlias = str | int | float | bool
BenchmarkResult: TypeAlias = dict[str, BenchmarkValue]
AlgorithmFunction: TypeAlias = Callable[[], BenchmarkResult]