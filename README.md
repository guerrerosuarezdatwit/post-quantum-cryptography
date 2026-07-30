# Post-Quantum Cryptography Benchmark

Implementation and performance evaluation of ML-KEM (FIPS 203) compared with classical public-key algorithms.

## Project Structure

```
post-quantum-cryptography/

src/
    mlkem_demo.py
    benchmark.py
    graphs.py
    config.py

results/
    plots/

README.md
requirements.txt
```

## Requirements

Python 3.12+

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running ML-KEM Demo

```bash
python src/mlkem_demo.py
```

## Running Benchmark

```bash
python src/benchmark.py
```

## Generating Graphs

```bash
python src/graphs.py
```

## Algorithms

- ML-KEM-768 (Implemented)
- RSA (Pending)
- ECDH (Pending)

## Notes

This project uses the Python implementation of the `mlkem` package implementing the NIST FIPS-203 ML-KEM standard.