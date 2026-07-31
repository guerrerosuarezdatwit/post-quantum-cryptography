"""
ECDH benchmark implementation.

Implements Elliptic Curve Diffie-Hellman (ECDH) key establishment for the
benchmarking framework. Generates key pairs, performs key exchange,
verifies correctness, and returns performance metrics.
"""

import os
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from benchmark_types import BenchmarkResult

CURVE = ec.SECP256R1()
SHARED_SECRET_SIZE = 32

def generate_keys() -> tuple[
    ec.EllipticCurvePrivateKey,
    ec.EllipticCurvePrivateKey,
]:
    """Generate EC key pairs for Alice and Bob."""

    alice_private = ec.generate_private_key(CURVE)
    bob_private = ec.generate_private_key(CURVE)

    return alice_private, bob_private


def perform_key_exchange(
    alice_private: ec.EllipticCurvePrivateKey,
    bob_private: ec.EllipticCurvePrivateKey,
) -> tuple[bytes, bytes]:
    """Derive the shared secret independently for both parties."""

    alice_secret = alice_private.exchange(
        ec.ECDH(),
        bob_private.public_key(),
    )

    bob_secret = bob_private.exchange(
        ec.ECDH(),
        alice_private.public_key(),
    )

    return alice_secret, bob_secret


def derive_aes_key(shared_secret: bytes) -> bytes:
    """Derive a 256-bit AES key from the raw ECDH shared secret."""

    return HKDF(
        algorithm=hashes.SHA256(),
        length=SHARED_SECRET_SIZE,
        salt=None,
        info=b"ecdh benchmark",
    ).derive(shared_secret)

def generate_keys() -> tuple[
    ec.EllipticCurvePrivateKey,
    ec.EllipticCurvePrivateKey,
]:
    """Generate EC key pairs for Alice and Bob."""

    alice_private = ec.generate_private_key(CURVE)
    bob_private = ec.generate_private_key(CURVE)

    return alice_private, bob_private


def perform_key_exchange(
    alice_private: ec.EllipticCurvePrivateKey,
    bob_private: ec.EllipticCurvePrivateKey,
) -> tuple[bytes, bytes]:
    """Derive the shared secret independently for both parties."""

    alice_secret = alice_private.exchange(
        ec.ECDH(),
        bob_private.public_key(),
    )

    bob_secret = bob_private.exchange(
        ec.ECDH(),
        alice_private.public_key(),
    )

    return alice_secret, bob_secret


def derive_aes_key(shared_secret: bytes) -> bytes:
    """Derive a 256-bit AES key from the raw ECDH shared secret."""

    return HKDF(
        algorithm=hashes.SHA256(),
        length=SHARED_SECRET_SIZE,
        salt=None,
        info=b"ecdh benchmark",
    ).derive(shared_secret)

def measure_key_sizes(
    alice_private: ec.EllipticCurvePrivateKey,
) -> tuple[int, int]:
    """Return serialized ECDH key sizes in bytes."""

    public_bytes = alice_private.public_key().public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    private_bytes = alice_private.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return len(public_bytes), len(private_bytes)

def ecdh_demo() -> BenchmarkResult:
    """
    Execute one ECDH benchmark iteration.

    Returns:
        BenchmarkResult containing timing, key sizes,
        shared secret size, and verification status.
    """

    # Generate Alice and Bob's key pairs.
    keygen_start = time.perf_counter()
    alice_private, bob_private = generate_keys()
    keygen_end = time.perf_counter()

    # Perform the ECDH key exchange.
    exchange_start = time.perf_counter()
    alice_secret, bob_secret = perform_key_exchange(
        alice_private,
        bob_private,
    )
    exchange_end = time.perf_counter()

    # Verify correctness using an AES-GCM round trip.
    verify_start = time.perf_counter()

    secrets_match = alice_secret == bob_secret

    alice_key = derive_aes_key(alice_secret)
    bob_key = derive_aes_key(bob_secret)

    nonce = b"\x00" * 12
    plaintext = os.urandom(32)

    ciphertext = AESGCM(alice_key).encrypt(
        nonce,
        plaintext,
        None,
    )

    recovered = AESGCM(bob_key).decrypt(
        nonce,
        ciphertext,
        None,
    )

    success = secrets_match and recovered == plaintext

    verify_end = time.perf_counter()

    public_key_size, private_key_size = measure_key_sizes(
        alice_private,
    )

    return {
        "algorithm": "ECDH-P256",
        "key_generation_ms": (keygen_end - keygen_start) * 1000,
        "encapsulation_ms": (exchange_end - exchange_start) * 1000,
        "decapsulation_ms": (verify_end - verify_start) * 1000,
        "exchange_ms": (
            (exchange_end - exchange_start)
            + (verify_end - verify_start)
        ) * 1000,
        "public_key_size": public_key_size,
        "private_key_size": private_key_size,
        "ciphertext_size": len(ciphertext),
        "shared_secret_size": SHARED_SECRET_SIZE,
        "success": success,
    }