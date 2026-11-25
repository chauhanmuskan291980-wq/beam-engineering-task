# Verification and Validation (V&V)

## 1. Verification

Verification checks whether the Python implementation correctly translates the engineering calculations defined in the source Excel workbook.

The following formulas were implemented:

- **Bending moment:** \(M = wL^2/8\)
- **Bending stress:** \(\sigma = M/S\)
- **Stress utilisation:** \(\sigma/f_y\)
- **Midspan deflection:** \(\delta = 5wL^4/(384EI)\)
- **Deflection limit:** \(L/n\)

All input values are converted into SI units before calculations. The implementation also supports Imperial inputs and returns results in both SI and Imperial units.

Automated tests were executed using `pytest` to check:
- Invalid inputs, including zero and negative values.
- Unsupported unit systems.
- Expected bending moment.
- Equivalence of SI and Imperial input calculations.
- Engineering outputs against independently evaluated workbook values.

The test suite passed successfully.

## 2. Validation

Validation checks whether the implementation meets the intended engineering requirements.

The Python results were compared with the expected results calculated from the source workbook for the reference beam:

| Parameter | Expected result |
|---|---:|
| Bending moment | 45 kN·m |
| Bending stress | 75.3769 MPa |
| Stress utilisation | 0.2741 |
| Midspan deflection | 9.9230 mm |
| Deflection limit | 16.6667 mm |
| Stress check | PASS |
| Deflection check | PASS |

The results agree with the independently evaluated workbook calculations.

## 3. Assumptions and Limitations

- The beam is simply supported.
- A uniformly distributed load acts over the full span.
- Linear-elastic Euler-Bernoulli beam theory is assumed.
- Material properties are assumed constant.
- The implementation checks bending stress and deflection only; it does not cover shear, buckling, fatigue, or other structural design requirements.

## 4. AI Usage Disclosure

ChatGPT was used as an assistance tool for code structuring, test-case suggestions, and documentation drafting. The implementation, engineering formulas, unit conversions, and test results were reviewed and executed independently by the developer.