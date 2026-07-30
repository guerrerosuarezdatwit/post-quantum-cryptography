# Post-Quantum Cryptography Benchmark
Benchmarking classical and post-quantum key establishment algorithms using a modular and reproducible evaluation framework.

A modular benchmarking framework for evaluating the performance of classical and post-quantum key establishment algorithms using reproducible statistical measurements.

This project was developed as part of an Applied Cryptography course to evaluate the performance characteristics of NIST standardized ML-KEM alongside classical key exchange algorithms.

---

## Project Goals

- Benchmark Post-Quantum Cryptography (ML-KEM-768)
- Compare ML-KEM against RSA and ECDH
- Measure execution time
- Measure key and ciphertext sizes
- Produce reproducible benchmark results
- Automatically generate visualizations

---

## Technologies

- Python 3.12
- ML-KEM (FIPS 203)
- mlkem Python library
- pandas
- matplotlib
- NumPy

---

## Current Status

| Algorithm | Status |
|-----------|--------|
| ML-KEM-768 | ✅ Complete |
| RSA | ⏳ Pending |
| ECDH | ⏳ Pending |

---

## Repository Structure

```
post-quantum-cryptography/
│
├── docs/
│   └── benchmark_methodology.md
│
├── results/
│   ├── plots/
│   └── *.csv
│
├── src/
│   ├── algorithms.py
│   ├── benchmark.py
│   ├── config.py
│   ├── graphs.py
│   ├── mlkem_demo.py
│   └── validation.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Features

- Modular benchmarking framework
- Automatic benchmark validation
- Statistical analysis
- CSV export
- Automatic graph generation
- Extensible architecture for additional algorithms

---


## Installation

Clone the repository:

```bash
git clone <repository-url>
cd post-quantum-cryptography
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Benchmark

```bash
python src/benchmark.py
```

The benchmark generates:

- Raw benchmark data
- Statistical summaries
- Combined benchmark summary

inside the `results/` directory.

---

## Generating Graphs

```bash
python src/graphs.py
```

The generated plots are saved to:

```
results/plots/
```

---

## Current ML-KEM Implementation

Implemented features:

- ML-KEM-768 key generation
- Encapsulation
- Decapsulation
- Shared secret verification
- Automatic benchmarking
- CSV export
- Statistical analysis
- Graph generation
- Benchmark validation

---

## Preliminary Results

Current benchmark results (Apple Silicon):

| Metric | Average |
|--------|---------:|
| Key Generation | ~0.21 ms |
| Encapsulation | ~0.31 ms |
| Decapsulation | ~0.37 ms |
| Total Exchange | ~0.68 ms |

Measured using 1000 benchmark iterations.

---

## Benchmark Methodology

Benchmark methodology is documented in:

```
docs/benchmark_methodology.md
```

The benchmark performs:

- 50 warm-up iterations
- 1000 measured iterations

Statistics include:

- Mean
- Median
- Standard deviation
- Minimum
- Maximum

---

## Future Work

- Implement RSA benchmarking
- Implement ECDH benchmarking
- Generate comparative performance graphs
- Perform statistical comparison
- Write final performance analysis

---

## References

- NIST FIPS 203 - Module-Lattice-Based Key-Encapsulation Mechanism (ML-KEM)
- NIST Post-Quantum Cryptography Standardization Project

---

## Acknowledgements

This project was developed for the Applied Cryptography course and follows the NIST Post-Quantum Cryptography standardization effort.

---

## License

This repository is intended for educational and research purposes.