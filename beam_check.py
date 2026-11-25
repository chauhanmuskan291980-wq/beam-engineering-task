import math

# Imperial to SI conversion factors
FT_TO_M = 0.3048
KIP_PER_FT_TO_N_PER_M = 14593.9029372
IN3_TO_M3 = 1.6387064e-5
IN4_TO_M4 = 4.162314256e-7
KSI_TO_PA = 6894757.293

# SI to Imperial conversion factors
NM_TO_KIP_FT = 0.000737562149277
M_TO_IN = 39.37007874

def convert_to_si(
    span,
    uniform_load,
    section_modulus,
    second_moment_of_area,
    youngs_modulus,
    yield_strength,
    unit_system
):
    """
    Convert beam input properties into SI units.

    SI inputs:
        span: m
        uniform_load: kN/m
        section_modulus: cm³
        second_moment_of_area: cm⁴
        youngs_modulus: GPa
        yield_strength: MPa

    Imperial inputs:
        span: ft
        uniform_load: kip/ft
        section_modulus: in³
        second_moment_of_area: in⁴
        youngs_modulus: ksi
        yield_strength: ksi

    Returns:
        Dictionary containing SI values.
    """

    if unit_system == "SI":
        return {
            "span_m": span,
            "load_n_per_m": uniform_load * 1000,
            "section_modulus_m3": section_modulus * 1e-6,
            "second_moment_m4": second_moment_of_area * 1e-8,
            "youngs_modulus_pa": youngs_modulus * 1e9,
            "yield_strength_pa": yield_strength * 1e6
        }

    elif unit_system == "Imperial":
        return {
            "span_m": span * FT_TO_M,
            "load_n_per_m": uniform_load * KIP_PER_FT_TO_N_PER_M,
            "section_modulus_m3": section_modulus * IN3_TO_M3,
            "second_moment_m4": second_moment_of_area * IN4_TO_M4,
            "youngs_modulus_pa": youngs_modulus * KSI_TO_PA,
            "yield_strength_pa": yield_strength * KSI_TO_PA
        }

    else:
        raise ValueError("Unsupported unit system")



def calculate_beam_check(
    span,
    uniform_load,
    section_modulus,
    second_moment_of_area,
    youngs_modulus,
    yield_strength,
    deflection_ratio,
    unit_system="SI"
):
    """
    Calculate bending stress, stress utilisation and beam deflection.

    All calculations are performed internally in SI units.

    Returns:
        SI results, Imperial results, workbook-compatible results,
        and PASS/FAIL checks.
    """

    # 1. Validate unit system
    if unit_system not in ("SI", "Imperial"):
        raise ValueError("Unsupported unit system")

    # 2. Validate numerical inputs
    inputs = {
        "span": span,
        "uniform_load": uniform_load,
        "section_modulus": section_modulus,
        "second_moment_of_area": second_moment_of_area,
        "youngs_modulus": youngs_modulus,
        "yield_strength": yield_strength,
        "deflection_ratio": deflection_ratio
    }

    for name, value in inputs.items():
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value <= 0
        ):
            raise ValueError(f"{name} must be a finite number greater than zero")

    # 3. Convert inputs into SI units
    si = convert_to_si(
        span,
        uniform_load,
        section_modulus,
        second_moment_of_area,
        youngs_modulus,
        yield_strength,
        unit_system
    )

    # 4. Extract converted properties
    L = si["span_m"]
    w = si["load_n_per_m"]
    S = si["section_modulus_m3"]
    I = si["second_moment_m4"]
    E = si["youngs_modulus_pa"]
    fy = si["yield_strength_pa"]

    # 5. Calculate maximum bending moment
    # M = wL² / 8
    bending_moment_n_m = (w * L**2) / 8

    # 6. Calculate bending stress
    # sigma = M / S
    bending_stress_pa = bending_moment_n_m / S
    bending_stress_mpa = bending_stress_pa / 1e6

    # 7. Calculate stress utilisation
    # U = sigma / fy
    stress_utilisation = bending_stress_pa / fy

    stress_check = (
        "PASS" if stress_utilisation <= 1 else "FAIL"
    )

    # 8. Calculate maximum midspan deflection
    # delta = 5wL⁴ / 384EI
    deflection_m = (5 * w * L**4) / (384 * E * I)

    # 9. Calculate permitted deflection
    deflection_limit_m = L / deflection_ratio

    deflection_check = (
        "PASS"
        if deflection_m <= deflection_limit_m
        else "FAIL"
    )

    # 10. Convert results into Imperial units
    bending_moment_kip_ft = bending_moment_n_m * NM_TO_KIP_FT
    bending_stress_ksi = bending_stress_pa / KSI_TO_PA

    deflection_inches = deflection_m * M_TO_IN
    deflection_limit_inches = deflection_limit_m * M_TO_IN

    # 11. Return all results
    return {
        "si": {
            "bending_moment_n_m": bending_moment_n_m,
            "bending_stress_pa": bending_stress_pa,
            "deflection_m": deflection_m,
            "deflection_limit_m": deflection_limit_m
        },

        "imperial": {
            "bending_moment_kip_ft": bending_moment_kip_ft,
            "bending_stress_ksi": bending_stress_ksi,
            "deflection_inches": deflection_inches,
            "deflection_limit_inches": deflection_limit_inches
        },

        "workbook_units": {
            "bending_moment_kn_m": bending_moment_n_m / 1000,
            "bending_stress_mpa": bending_stress_mpa,
            "stress_utilisation": stress_utilisation,
            "deflection_mm": deflection_m * 1000,
            "deflection_limit_mm": deflection_limit_m * 1000
        },

        "checks": {
            "stress": stress_check,
            "deflection": deflection_check
        }
    }




def display_results(result):
    """Display SI, Imperial and workbook-unit results."""

    si = result["si"]
    imperial = result["imperial"]
    workbook = result["workbook_units"]
    checks = result["checks"]

    print("\n========== SI RESULTS ==========")

    print(f"Bending Moment:       {si['bending_moment_n_m']:.2f} N·m")
    print(f"Bending Stress:       {si['bending_stress_pa'] / 1e6:.2f} MPa")
    print(f"Deflection:           {si['deflection_m'] * 1000:.2f} mm")
    print(f"Deflection Limit:     {si['deflection_limit_m'] * 1000:.2f} mm")

    print("\n========== IMPERIAL RESULTS ==========")

    print(f"Bending Moment:       {imperial['bending_moment_kip_ft']:.2f} kip·ft")
    print(f"Bending Stress:       {imperial['bending_stress_ksi']:.2f} ksi")
    print(f"Deflection:           {imperial['deflection_inches']:.2f} inches")
    print(f"Deflection Limit:     {imperial['deflection_limit_inches']:.2f} inches")

    print("\n========== WORKBOOK RESULTS ==========")

    print(f"Bending Moment:       {workbook['bending_moment_kn_m']:.2f} kN·m")
    print(f"Bending Stress:       {workbook['bending_stress_mpa']:.2f} MPa")
    print(f"Stress Utilisation:   {workbook['stress_utilisation']:.4f}")
    print(f"Deflection:           {workbook['deflection_mm']:.2f} mm")
    print(f"Deflection Limit:     {workbook['deflection_limit_mm']:.2f} mm")

    print("\n========== ENGINEERING CHECKS ==========")

    print(f"Stress Check:         {checks['stress']}")
    print(f"Deflection Check:     {checks['deflection']}")


if __name__ == "__main__":

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

    display_results(result)