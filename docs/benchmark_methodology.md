# Benchmark Methodology

## Environment

- Hardware: Apple MacBook Pro M1
- Operating system: macOS Tahoe 26.5.2
- Python: 3.12.13
- Benchmark iterations: 1000
- Warm-up iterations: 50
- Timing function: time.perf_counter()

---

## Algorithms

Current:

- ML-KEM-768 (Implemented)

Pending:

- RSA
- ECDH

---

## Timing Definitions

### Key Generation

Measures only the generation of cryptographic key material.

### Exchange Time

Measures only the secure key exchange operation.

For each algorithm:

- ML-KEM: Encapsulation + Decapsulation
- RSA: Encryption + Decryption of a random 32-byte secret
- ECDH: Shared secret computation by both participants

Key generation is NOT included in exchange time.

---

## Correctness Validation

Each benchmark iteration verifies that both parties compute the same
shared secret.

If validation fails, benchmarking stops.

---

## Size Measurements

The benchmark records:

- Public key size
- Private key size
- Ciphertext size
- Shared secret size

---

## Benchmark Notes

- 50 warm-up executions are discarded.
- 1000 iterations are measured.
- Results are summarized using:
  - Mean
  - Median
  - Standard deviation
  - Minimum
  - Maximum

---

## Limitations

Results depend on:

- Hardware
- Operating System
- Python implementation
- Cryptographic library implementation
- System load

These measurements evaluate implementation performance only and do not
represent theoretical algorithmic complexity.