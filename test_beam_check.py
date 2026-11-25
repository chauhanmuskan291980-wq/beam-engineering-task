
import pytest

from beam_check import calculate_beam_check


def valid_si_inputs():
    """Return a standard set of valid SI inputs."""
    return {
        "span": 6,
        "uniform_load": 10,
        "section_modulus": 597,
        "second_moment_of_area": 8503,
        "youngs_modulus": 200,
        "yield_strength": 275,
        "deflection_ratio": 360,
        "unit_system": "SI",
    }


@pytest.mark.parametrize(
    "input_name, invalid_value",
    [
        ("span", 0),
        ("span", -1),
        ("uniform_load", 0),
        ("uniform_load", -10),
        ("section_modulus", 0),
        ("second_moment_of_area", -1),
        ("youngs_modulus", 0),
        ("yield_strength", -5),
        ("deflection_ratio", 0),
    ],
)
def test_invalid_inputs_raise_value_error(input_name, invalid_value):
    """Every physical input must be greater than zero."""
    inputs = valid_si_inputs()
    inputs[input_name] = invalid_value

    with pytest.raises(ValueError):
        calculate_beam_check(**inputs)


def test_unsupported_unit_system():
    """Unsupported unit systems must raise ValueError."""
    inputs = valid_si_inputs()
    inputs["unit_system"] = "XYZ"

    with pytest.raises(ValueError, match="Unsupported unit system"):
        calculate_beam_check(**inputs)


def test_si_bending_moment():
    """Check the SI bending moment against the expected result."""
    result = calculate_beam_check(**valid_si_inputs())

    assert result["si"]["bending_moment_n_m"] == pytest.approx(
        45000,
        abs=0.01,
    )


def test_si_and_imperial_results_are_equivalent():
    """Equivalent SI and Imperial inputs should produce matching SI results."""

    si_result = calculate_beam_check(**valid_si_inputs())

    imperial_result = calculate_beam_check(
        span=19.6850393701,
        uniform_load=0.6852176586,
        section_modulus=36.4311752246,
        second_moment_of_area=204.2853921408,
        youngs_modulus=29007.54754675,
        yield_strength=39.8853778768,
        deflection_ratio=360,
        unit_system="Imperial",
    )

    assert imperial_result["si"]["bending_moment_n_m"] == pytest.approx(
        si_result["si"]["bending_moment_n_m"],
        rel=1e-5,
    )

    assert imperial_result["si"]["bending_stress_pa"] == pytest.approx(
        si_result["si"]["bending_stress_pa"],
        rel=1e-5,
    )

    assert imperial_result["si"]["deflection_m"] == pytest.approx(
        si_result["si"]["deflection_m"],
        rel=1e-5,
    )



def test_si_results_match_workbook():
    """Verify all SI results against expected workbook calculations."""

    result = calculate_beam_check(**valid_si_inputs())
    workbook = result["workbook_units"]

    assert workbook["bending_moment_kn_m"] == pytest.approx(45.0)
    assert workbook["bending_stress_mpa"] == pytest.approx(75.376884422)
    assert workbook["stress_utilisation"] == pytest.approx(0.2740977615)
    assert workbook["deflection_mm"] == pytest.approx(9.922968364)
    assert workbook["deflection_limit_mm"] == pytest.approx(16.666666667)

    assert result["checks"]["stress"] == "PASS"
    assert result["checks"]["deflection"] == "PASS"
