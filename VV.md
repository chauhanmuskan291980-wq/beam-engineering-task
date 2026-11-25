# Verification and Validation (V&V)

## 1. Validation – Are These the Right Equations?

The implementation models a simply supported beam subjected to a uniformly distributed load (UDL) over its full span. The governing equations are:

- Maximum bending moment: \(M = wL^2/8\)
- Bending stress: \(\sigma = M/S\)
- Stress utilisation: \(U = \sigma/f_y\)
- Maximum midspan deflection: \(\delta = 5wL^4/(384EI)\)
- Deflection limit: \(\delta_{\text{limit}} = L/n\)

The beam equations were checked against the *FAO, Structural Design Handbook*, Chapter 7, Table 7.1. The bending stress equation uses the standard elastic flexure relationship.

**Assumptions:** Simply supported beam, full-span UDL, constant material properties, and linear-elastic Euler–Bernoulli beam theory. The checks cover bending stress and deflection only.

## 2. Verification – Does the Code Solve Them Correctly?

The Python implementation was checked against independently evaluated workbook formulas using the pre-filled inputs.

| Output | Workbook value | Python value | Tolerance |
|---|---:|---:|---:|
| Bending moment (kN·m) | 45.0000 | 45.0000 | ±0.01 |
| Bending stress (MPa) | 75.3769 | 75.3769 | ±0.0001 |
| Stress utilisation | 0.2741 | 0.2741 | ±0.000001 |
| Deflection (mm) | 9.9230 | 9.9230 | ±0.0001 |
| Deflection limit (mm) | 16.6667 | 16.6667 | ±0.0001 |
| Stress check | PASS | PASS | Exact match |
| Deflection check | PASS | PASS | Exact match |

Tolerances account for numerical precision and rounding in displayed results. PASS/FAIL results require exact agreement.

Automated tests using `pytest` cover invalid inputs, unsupported unit systems, expected bending moment, SI/Imperial equivalence, and workbook calculation results. All 13 tests passed.

**Undocumented workbook constant:** The value `100000` in the deflection calculation was identified as a combined unit-conversion factor. It results from converting kN to N, metres to millimetres, GPa to Pa, and cm⁴ to m⁴:

\[
\frac{10^3 \times 10^3}{10^9 \times 10^{-8}}=10^5
\]

The Python implementation performs these conversions explicitly rather than relying on this unexplained constant.

## 3. Unit Conversion References

Imperial inputs are converted to SI at the input boundary. Factors used include:

- ft to m: 0.3048
- kip/ft to N/m: 14593.9029372
- in³ to m³: 1.6387064 × 10⁻⁵
- in⁴ to m⁴: 4.162314256 × 10⁻⁷
- ksi to Pa: 6894757.293

The force, pressure, and length conversion factors were checked against the [NIST Guide to the SI, Appendix B](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors). Area and volume-related geometric conversions were derived from the exact inch-to-metre conversion.

## 4. AI Usage Disclosure

ChatGPT was used to assist with understanding workbook formulas, code structuring, test-case suggestions, and documentation.

A significant item independently checked was the undocumented `100000` constant. Its origin was verified by deriving the combined unit conversions mathematically and comparing the resulting deflection with the independently evaluated workbook formula. Unit conversions and test results were also reviewed and executed locally.

**Workbook note:** Stored Excel formula results were unavailable for direct comparison, so expected values were independently evaluated from the workbook formulas.