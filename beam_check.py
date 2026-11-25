def convert_to_si(
    span,
    uniform_load,
    section_modulus,
    second_moment_of_area,
    youngs_modulus,
    yield_strength,
    unit_system
):
    if unit_system == "SI":
        span_m=span
        load_n_per_m = uniform_load * 1000
        section_modulus_m3 = section_modulus * 1e-6
        second_moment_m4 = second_moment_of_area * 1e-8
        youngs_modulus_pa = youngs_modulus*1e9
        yield_strength_pa = yield_strength*1e6

    elif unit_system == "Imperial":
        span_m = span * 0.3048
        load_n_per_m = uniform_load * 14593.9029372
        section_modulus_m3 = section_modulus  * 1.6387064e-5
        second_moment_m4 = second_moment_of_area * 4.162314256e-7
        youngs_modulus_pa = youngs_modulus * 6894757.293
        yield_strength_pa = yield_strength * 6894757.293
    else:
        raise ValueError("Unsupported unit system")

    return {
        "span_m":span_m,
        "load_n_per_m":load_n_per_m,
        "section_modulus_m3":section_modulus_m3,
        "second_moment_m4":second_moment_m4,
        "youngs_modulus_pa":youngs_modulus_pa,
        "yield_strength_pa":yield_strength_pa
    }
















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

    if span <= 0:
        raise ValueError("Span must be greater than zero")

    if uniform_load <= 0:
        raise ValueError("Uniform load must be greater than zero")

    if section_modulus <= 0:
        raise ValueError("Section modulus must be greater than zero")

    if second_moment_of_area <= 0:
        raise ValueError("Second moment of area must be greater than zero")

    if youngs_modulus <= 0:
        raise ValueError("Young's modulus must be greater than zero")

    if yield_strength <= 0:
        raise ValueError("Yield strength must be greater than zero")

    if deflection_ratio <= 0:
        raise ValueError("Deflection ratio must be greater than zero")

    if unit_system not in ("SI", "Imperial"):
        raise ValueError("Unsupported unit system")

    # Convert all input values into SI base units
    si_values = convert_to_si(
    span,
    uniform_load,
    section_modulus,
    second_moment_of_area,
    youngs_modulus,
    yield_strength,
    unit_system
)
    # extract converted values
    span_m = si_values['span_m']
    load_n_per_m = si_values["load_n_per_m"]

    # Calculate maximum bending moment
    bending_moment_n_m = (load_n_per_m*span_m**2)/8

    # Extract section modulus 
    section_modulus_m3 = si_values["section_modulus_m3"]

    # Calculate bending stress
    bending_stress_pa = bending_moment_n_m/ section_modulus_m3

    # Convert stress into MPa for workbook-compataible output
    bending_stress_mpa = bending_stress_pa / 1e6


    # Extract yield strength
    yield_strength_pa = si_values['yield_strength_pa']

    # Calculate stress utilisation 
    stress_utilisation = bending_stress_pa / yield_strength_pa

    # Determine stress check
    stress_check = "PASS" if stress_utilisation <=1 else "FAIL"







    return {
    "bending_moment_n_m": bending_moment_n_m,
    "bending_stress_pa": bending_stress_pa,
    "bending_stress_mpa": bending_stress_mpa,
    "stress_utilisation": stress_utilisation,
    "stress_check": stress_check
}



if __name__ == "__main__":

    result = calculate_beam_check(
        span=6,
        uniform_load=10,
        section_modulus=597,
        second_moment_of_area=8503,
        youngs_modulus=200,
        yield_strength=275,
        deflection_ratio=360,
        unit_system="SI",
    )

    print(result)