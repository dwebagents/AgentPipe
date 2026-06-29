import pytest

from turbo_encabulator import (
    EncabulatorValueError,
    SpurvingPathError,
    TurboEncabulator,
    TurboEncabulatorConfig,
    anti_grunch,
    build_default_turbo_encabulator,
    encabulate,
    reduce_sinusoidal_repleneration,
    validate_spurving_path,
)


def test_default_encabulator_synchronizes_cardinal_grammeters():
    report = build_default_turbo_encabulator().encabulate()

    assert report.cardinal_grammeters_synchronized is True
    assert report.side_fumbling_prevented is True
    assert report.effective_grunch_index == 0.27
    assert report.inverse_reactive_current == 4.38
    assert report.sinusoidal_repleneration == 1.0
    assert report.spurving_path == (
        (-1.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
    )
    assert report.warnings == ()


def test_spurving_path_validation_normalizes_a_direct_line():
    path = validate_spurving_path([(-2, 0, 0), (0, 0, 0), (2, 0, 0)])

    assert path == (
        (-2.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (2.0, 0.0, 0.0),
    )


def test_spurving_path_validation_rejects_sideways_fan():
    with pytest.raises(SpurvingPathError, match="direct line"):
        validate_spurving_path([(-1, 0, 0), (0, 1, 0), (1, 0, 0)])


def test_spurving_path_validation_rejects_collapsed_segments():
    with pytest.raises(SpurvingPathError, match="collapse"):
        validate_spurving_path([(-1, 0, 0), (-1, 0, 0), (1, 0, 0)])


def test_anti_grunching_clamps_and_reduces_risk():
    assert anti_grunch(1.7) == 0.65
    assert anti_grunch(0.62) == 0.27
    assert anti_grunch(-4) == 0.0


def test_dingle_arm_reduces_sinusoidal_repleneration():
    unassisted = reduce_sinusoidal_repleneration(4, dingle_arm_engaged=False)
    assisted = reduce_sinusoidal_repleneration(4, dingle_arm_engaged=True)

    assert unassisted == 1.8
    assert assisted == 0.99
    assert assisted < unassisted


def test_misconfigured_tremie_pipe_blocks_synchronization_with_warning():
    config = TurboEncabulatorConfig(marzlevanes=5, tremie_pipe_reversible=True)
    report = TurboEncabulator(config).encabulate()

    assert report.cardinal_grammeters_synchronized is False
    assert report.side_fumbling_prevented is False
    assert "six hydrocoptic marzlevanes are required" in report.warnings
    assert "tremie pipe must be non-reversible" in report.warnings


def test_encabulation_reports_are_deterministic_for_same_configuration():
    config = TurboEncabulatorConfig(novertrunnion_load=3.5, dingle_arm_engaged=True)

    assert encabulate(config) == encabulate(config)


def test_non_finite_values_are_rejected():
    with pytest.raises(EncabulatorValueError, match="finite"):
        encabulate(magneto_reluctance=float("nan"))
