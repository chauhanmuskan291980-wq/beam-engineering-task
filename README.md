# Beam Engineering Calculation – Python

A verified Python implementation of a simply supported steel beam calculation, translated from an Excel engineering workbook.

The application evaluates **bending stress** and **midspan deflection** under a uniformly distributed load (UDL). It supports both SI and Imperial input systems, performs calculations internally using SI units, and reports results in both systems.

## Overview

This project converts an existing Excel engineering calculation into a structured and tested Python implementation.

The calculation evaluates:

- Maximum bending moment
- Bending stress
- Stress utilisation
- Maximum midspan deflection
- Allowable deflection limit
- Stress and deflection PASS/FAIL checks

The implementation includes input validation, unit conversion, automated tests, and Verification & Validation documentation.

## Engineering Equations

The implementation uses the following standard beam equations:

| Calculation | Formula |
|---|---|
| Maximum bending moment | \(M = wL^2/8\) |
| Bending stress | \(\sigma = M/S\) |
| Stress utilisation | \(U = \sigma/f_y\) |
| Maximum midspan deflection | \(\delta = 5wL^4/(384EI)\) |
| Deflection limit | \(\delta_{\text{limit}} = L/n\) |

Where:

- \(L\) = Beam span
- \(w\) = Uniformly distributed load
- \(S\) = Section modulus
- \(I\) = Second moment of area
- \(E\) = Young's modulus
- \(f_y\) = Yield strength
- \(n\) = Deflection ratio

## Features

- **SI and Imperial support:** Accepts engineering inputs in both unit systems.
- **SI-based calculations:** Converts all input values into SI units before performing calculations.
- **Dual-unit reporting:** Returns results in SI and Imperial units, along with the original workbook units.
- **Input validation:** Rejects zero, negative, non-finite, and invalid numerical inputs.
- **Engineering checks:** Evaluates bending stress and deflection against their respective limits.
- **Automated testing:** Uses pytest to verify calculations, input validation, and unit-system equivalence.
- **Structured output:** Returns calculation results in a structured Python dictionary.

## Project Structure

```text
beam-engineering-task/
│
├── beam_check.py          # Engineering calculations and unit conversions
├── test_beam_check.py     # Automated pytest test suite
├── source_workbook.xlsx   # Original Excel calculation
├── requirements.txt       # Python dependencies
├── VV.md                  # Verification and Validation documentation
├── README.md              # Project documentation
└── .gitignore             # Excluded files and folders
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/beam-engineering-task.git
cd beam-engineering-task
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the engineering calculation:

```bash
python beam_check.py
```

The default reference inputs are:

| Parameter | Value | Unit |
|---|---:|---|
| Beam span | 6 | m |
| Uniform load | 10 | kN/m |
| Section modulus | 597 | cm³ |
| Second moment of area | 8503 | cm⁴ |
| Young's modulus | 200 | GPa |
| Yield strength | 275 | MPa |
| Deflection ratio | 360 | - |

The calculation function also supports Imperial inputs through the `unit_system` argument.

Example:

```python
from beam_check import calculate_beam_check

result = calculate_beam_check(
    span=6,
    uniform_load=10,
    section_modulus=597,
    second_moment_of_area=8503,
    youngs_modulus=200,
    yield_strength=275,
    deflection_ratio=360,
    unit_system="SI"
)

print(result)
```

To use Imperial inputs, provide the corresponding values in ft, kip/ft, in³, in⁴, and ksi, and set:

```python
unit_system="Imperial"
```

## Reference Calculation Results

For the pre-filled workbook inputs, the expected results are:

| Output | Expected result |
|---|---:|
| Bending moment | 45.00 kN·m |
| Bending stress | 75.38 MPa |
| Stress utilisation | 0.2741 |
| Midspan deflection | 9.92 mm |
| Deflection limit | 16.67 mm |
| Stress check | PASS |
| Deflection check | PASS |

### Sample Output

```text
========== WORKBOOK RESULTS ==========

Bending Moment:       45.00 kN·m
Bending Stress:       75.38 MPa
Stress Utilisation:   0.2741
Deflection:           9.92 mm
Deflection Limit:     16.67 mm

========== ENGINEERING CHECKS ==========

Stress Check:         PASS
Deflection Check:     PASS
```

## Running Tests

Run the automated test suite:

```bash
python -m pytest -v
```

The test suite checks:

- Invalid input handling
- Unsupported unit systems
- Expected bending moment
- SI and Imperial calculation equivalence
- Results against independently evaluated workbook calculations

## Assumptions and Limitations

- The beam is simply supported.
- A uniformly distributed load acts over the full span.
- Linear-elastic Euler-Bernoulli beam theory is assumed.
- Material properties are constant.
- The implementation checks bending stress and deflection only.
- Shear, buckling, fatigue, and other structural design checks are outside the scope of this project.

## Verification and Validation

The implementation is documented and evaluated in [`VV.md`](VV.md).

This document covers:

- Engineering equation validation
- Verification against reference workbook calculations
- Numerical tolerances
- Unit conversion methodology
- The undocumented unit-conversion constant identified in the source workbook
- AI usage disclosure

## Technologies Used

- Python 3
- pytest
- Excel (source calculation workbook)
- Git and GitHub

## Author

**Muskan Chauhan**

Software Engineer | Backend & Applied AI Engineering

GitHub: https://github.com/chauhanmuskan291980-wq

---

*Developed as part of the Software Engineer I take-home assessment for Mahavidya Services Private Limited.*