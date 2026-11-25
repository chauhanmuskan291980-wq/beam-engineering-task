def convert_to_si(
    span,
    uniform_load,
    section_modulus,
    second_moment_of_area,
    youngs_modulus,
    yield_strength,
    unit_system
):
    pass















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

    return "Inputs are valid"