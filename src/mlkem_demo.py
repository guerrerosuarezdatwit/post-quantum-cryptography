from time import perf_counter

from mlkem.ml_kem import ML_KEM
from mlkem.parameter_set import ML_KEM_768


def mlkem_demo() -> dict[str, int | float | str | bool]:
    """
    Run one ML-KEM-768 key-establishment operation.

    Returns timing, size, and correctness information using the common
    interface shared with the RSA and ECDH implementations.
    """

    ml_kem = ML_KEM(ML_KEM_768, fast=True)

    # Alice generates the encapsulation and decapsulation keys.
    keygen_start = perf_counter()
    encapsulation_key, decapsulation_key = ml_kem.key_gen()
    keygen_end = perf_counter()

    # Bob uses Alice's public encapsulation key to create a ciphertext
    # and shared secret.
    encaps_start = perf_counter()
    bob_secret, ciphertext = ml_kem.encaps(encapsulation_key)
    encaps_end = perf_counter()

    # Alice uses her private decapsulation key and Bob's ciphertext
    # to recover the same shared secret.
    decaps_start = perf_counter()
    alice_secret = ml_kem.decaps(decapsulation_key, ciphertext)
    decaps_end = perf_counter()

    secrets_match = alice_secret == bob_secret

    return {
        "algorithm": "ML-KEM-768",
        "key_generation_ms": (keygen_end - keygen_start) * 1000,
        "encapsulation_ms": (encaps_end - encaps_start) * 1000,
        "decapsulation_ms": (decaps_end - decaps_start) * 1000,
        "exchange_ms": (
            (encaps_end - encaps_start)
            + (decaps_end - decaps_start)
        )
        * 1000,
        "public_key_size": len(encapsulation_key),
        "private_key_size": len(decapsulation_key),
        "ciphertext_size": len(ciphertext),
        "shared_secret_size": len(bob_secret),
        "success": secrets_match,
    }


def main() -> None:
    result = mlkem_demo()

    print("=== ML-KEM-768 Demo ===")
    print(f"Key generation:   {result['key_generation_ms']:.4f} ms")
    print(f"Encapsulation:    {result['encapsulation_ms']:.4f} ms")
    print(f"Decapsulation:    {result['decapsulation_ms']:.4f} ms")
    print(f"Total exchange:   {result['exchange_ms']:.4f} ms")
    print()
    print(f"Public key size:  {result['public_key_size']} bytes")
    print(f"Private key size: {result['private_key_size']} bytes")
    print(f"Ciphertext size:  {result['ciphertext_size']} bytes")
    print(f"Shared secret:    {result['shared_secret_size']} bytes")
    print()
    print(f"Shared secrets match: {result['success']}")


if __name__ == "__main__":
    main()



