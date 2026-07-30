from typing import Any


REQUIRED_FIELDS = {
    "algorithm",
    "key_generation_ms",
    "exchange_ms",
    "public_key_size",
    "private_key_size",
    "shared_secret_size",
    "success",
}


def validate_benchmark_result(result: dict[str, Any]) -> None:
    """
    Validate that every benchmark implementation returns
    the expected interface.
    """

    missing = REQUIRED_FIELDS - result.keys()

    if missing:
        raise ValueError(
            f"Missing required fields: {sorted(missing)}"
        )

    if not isinstance(result["algorithm"], str):
        raise TypeError(
            "algorithm must be a string."
        )

    if not isinstance(result["success"], bool):
        raise TypeError(
            "success must be a boolean."
        )

    numeric_fields = REQUIRED_FIELDS - {
        "algorithm",
        "success",
    }

    for field in numeric_fields:
        value = result[field]

        if not isinstance(value, (int, float)):
            raise TypeError(
                f"{field} must be numeric."
            )

        if value < 0:
            raise ValueError(
                f"{field} cannot be negative."
            )