"""
RSA benchmark implementation.

Implements RSA public-key encryption for the benchmarking framework.
Generates a key pair, encrypts a randomly generated shared secret,
decrypts it, verifies correctness, and returns performance metrics.
"""

import os
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from benchmark_types import BenchmarkResult

KEY_SIZE = 2048
SHARED_SECRET_SIZE = 32

OAEP_PADDING = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)


def generate_keys() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair."""

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=KEY_SIZE,
    )

    public_key = private_key.public_key()

    return private_key, public_key


def encrypt_message(
    public_key: rsa.RSAPublicKey,
    plaintext: bytes,
) -> bytes:
    """Encrypt plaintext using the RSA public key."""

    return public_key.encrypt(plaintext, OAEP_PADDING)


def decrypt_message(
    private_key: rsa.RSAPrivateKey,
    ciphertext: bytes,
) -> bytes:
    """Decrypt ciphertext using the RSA private key."""

    return private_key.decrypt(ciphertext, OAEP_PADDING)


def measure_key_sizes(
    private_key: rsa.RSAPrivateKey,
    public_key: rsa.RSAPublicKey,
) -> tuple[int, int]:
    """Return serialized key sizes in bytes."""

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return len(public_bytes), len(private_bytes)


def rsa_demo() -> BenchmarkResult:
    """
    Execute one RSA benchmark iteration.

    Returns:
        BenchmarkResult containing timing, key sizes,
        ciphertext size, and verification status.
    """

    shared_secret = os.urandom(SHARED_SECRET_SIZE)

    start = time.perf_counter()
    private_key, public_key = generate_keys()
    key_generation_ms = (time.perf_counter() - start) * 1000

    public_key_size, private_key_size = measure_key_sizes(
        private_key,
        public_key,
    )

    start = time.perf_counter()
    ciphertext = encrypt_message(public_key, shared_secret)
    encryption_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    recovered_secret = decrypt_message(private_key, ciphertext)
    decryption_ms = (time.perf_counter() - start) * 1000

    success = recovered_secret == shared_secret

    return {
        "algorithm": f"RSA-{KEY_SIZE}",
        "key_generation_ms": key_generation_ms,
        "encapsulation_ms": encryption_ms,
        "decapsulation_ms": decryption_ms,
        "exchange_ms": encryption_ms + decryption_ms,
        "public_key_size": public_key_size,
        "private_key_size": private_key_size,
        "ciphertext_size": len(ciphertext),
        "shared_secret_size": SHARED_SECRET_SIZE,
        "success": success,
    }