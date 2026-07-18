"""Experiment runners for thesis CTMLM sensitivity experiments."""

from __future__ import annotations

import pandas as pd

from .parameters import CTMLMParameters
from .model import run_model


def final_state(sol) -> dict[str, float]:
    """Return final model state from a SciPy solution object."""
    return {
        "z_b": float(sol.y[0, -1]),
        "s_b": float(sol.y[1, -1]),
        "q_b": float(sol.y[2, -1]),
        "C": float(sol.y[3, -1]),
        "success": bool(sol.success),
    }


def run_experiment(
    name: str,
    params: CTMLMParameters,
    days: float = 300.0,
    y0=None,
) -> dict[str, float | str | bool]:
    """Run one named experiment and return a flat result dictionary."""
    sol = run_model(params=params, y0=y0, days=days)
    state = final_state(sol)

    return {
        "experiment_name": name,
        "D": params.D,
        "SST": params.SST,
        "U": params.U,
        "s_plus": params.s_plus,
        "s_surface": params.s_surface,
        "q_surface": params.q_surface,
        "delta_F": params.delta_F,
        **state,
    }


def _add_response_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add response columns relative to the control experiment."""
    out = df.copy()
    control = out.loc[out["experiment_name"] == "Control"].iloc[0]
    out["dC"] = out["C"] - control["C"]
    out["dz_b"] = out["z_b"] - control["z_b"]
    out["ds_b"] = out["s_b"] - control["s_b"]
    out["dq_b"] = out["q_b"] - control["q_b"]
    return out


def run_standard_experiments(days: float = 300.0) -> pd.DataFrame:
    """Run standard thesis sensitivity experiments.

    Experiments include control, weaker subsidence, SST warming, wind changes,
    inversion-strength changes, and a combined forcing case.
    """
    control = CTMLMParameters()

    experiments = [
        ("Control", control),
        ("Weaker subsidence", control.with_updates(D=control.D * 0.8)),
        ("Stronger subsidence", control.with_updates(D=control.D * 1.2)),
        (
            "SST warming",
            control.with_updates(
                SST=control.SST + 1.0,
                s_surface=control.s_surface + 1.0,
                q_surface=control.q_surface + 0.001,
            ),
        ),
        ("Weaker wind", control.with_updates(U=max(control.U - 1.0, 0.1))),
        ("Stronger wind", control.with_updates(U=control.U + 1.0)),
        (
            "Stronger inversion",
            control.with_updates(s_plus=control.s_plus + 1.0),
        ),
        (
            "Weaker subsidence + SST warming",
            control.with_updates(
                D=control.D * 0.8,
                SST=control.SST + 1.0,
                s_surface=control.s_surface + 1.0,
                q_surface=control.q_surface + 0.001,
            ),
        ),
    ]

    rows = [run_experiment(name, params, days=days) for name, params in experiments]
    return _add_response_columns(pd.DataFrame(rows))


def run_era5_guided_experiments(days: float = 300.0) -> pd.DataFrame:
    """Run ERA5-guided perturbation experiments for California and Namibia.

    The perturbation signs and magnitudes are based on the thesis ERA5 trend
    analysis. `D850_day` trends are converted from day-1 to s-1.
    """
    control = CTMLMParameters()

    trends = {
        "california": {
            "dSST": 0.326730,
            "dU": -0.128848,
            "dINV": 0.209065,
            "dD_day": -0.023895,
        },
        "namibia": {
            "dSST": 0.185904,
            "dU": 0.061032,
            "dINV": 0.153279,
            "dD_day": -0.001198,
        },
    }

    rows = []

    for region, tr in trends.items():
        dD = tr["dD_day"] / 86400.0
        dSST = tr["dSST"]
        dU = tr["dU"]
        dINV = tr["dINV"]

        scenarios = [
            ("Control", control),
            ("ERA5 D trend only", control.with_updates(D=max(control.D + dD, 1e-8))),
            (
                "ERA5 SST trend only",
                control.with_updates(
                    SST=control.SST + dSST,
                    s_surface=control.s_surface + dSST,
                ),
            ),
            ("ERA5 wind trend only", control.with_updates(U=max(control.U + dU, 0.1))),
            ("ERA5 inversion trend only", control.with_updates(s_plus=control.s_plus + dINV)),
            (
                "ERA5 combined trend forcing",
                control.with_updates(
                    D=max(control.D + dD, 1e-8),
                    SST=control.SST + dSST,
                    s_surface=control.s_surface + dSST,
                    U=max(control.U + dU, 0.1),
                    s_plus=control.s_plus + dINV,
                ),
            ),
        ]

        region_rows = []
        for name, params in scenarios:
            result = run_experiment(name, params, days=days)
            result["region"] = region
            result["dSST_forcing"] = dSST if "SST" in name or "combined" in name else 0.0
            result["dU_forcing"] = dU if "wind" in name or "combined" in name else 0.0
            result["dINV_forcing"] = dINV if "inversion" in name or "combined" in name else 0.0
            result["dD_forcing"] = dD if "D" in name or "combined" in name else 0.0
            region_rows.append(result)

        region_df = _add_response_columns(pd.DataFrame(region_rows))
        rows.append(region_df)

    return pd.concat(rows, ignore_index=True)
