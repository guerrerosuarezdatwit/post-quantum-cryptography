from mlkem_demo import mlkem_demo
from rsa_demo import rsa_demo
from ecdh_demo import ecdh_demo

from benchmark_types import AlgorithmFunction


# Central registry of algorithms available to the benchmark.
_ALGORITHMS: list[AlgorithmFunction] = [
    mlkem_demo,
    rsa_demo,
    ecdh_demo,
]


def get_algorithms() -> list[AlgorithmFunction]:
    """
    Return all registered cryptographic implementations.

    A copy is returned so callers cannot accidentally modify
    the central registry.
    """

    return _ALGORITHMS.copy()