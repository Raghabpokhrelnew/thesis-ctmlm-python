from thesis_ctmlm import CTMLMParameters, run_model, run_standard_experiments
from thesis_ctmlm.experiments import final_state


def test_model_runs_successfully():
    sol = run_model(days=5)
    assert sol.success


def test_final_state_has_expected_keys():
    sol = run_model(days=5)
    state = final_state(sol)
    for key in ["z_b", "s_b", "q_b", "C", "success"]:
        assert key in state


def test_cloud_fraction_is_physical():
    sol = run_model(days=5)
    state = final_state(sol)
    assert 0.0 <= state["C"] <= 1.0


def test_standard_experiments_return_dataframe():
    df = run_standard_experiments(days=5)
    assert "experiment_name" in df.columns
    assert "dC" in df.columns
    assert "dz_b" in df.columns
    assert len(df) >= 2


def test_parameter_updates_are_immutable():
    params = CTMLMParameters()
    new_params = params.with_updates(D=params.D * 0.8)
    assert new_params.D != params.D
    assert params.D == 4.0e-6
