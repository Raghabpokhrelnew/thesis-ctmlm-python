"""ODE system and solver for the thesis CTMLM model."""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy.integrate import solve_ivp

from .parameters import CTMLMParameters
from .thermodynamics import cloud_fraction_from_decoupling, clip_cloud_fraction
from .constants import SECONDS_PER_DAY


def surface_fluxes(s_b: float, q_b: float, params: CTMLMParameters) -> tuple[float, float]:
    """Bulk sensible and latent heat fluxes.

    Positive fluxes indicate energy or moisture input into the mixed layer.
    """
    shf = params.rho0 * params.cp * params.ce * params.U * (params.s_surface - s_b)
    lhf = params.rho0 * params.lv * params.ce * params.U * (params.q_surface - q_b)
    return shf, lhf


def entrainment_velocity(z_b: float, C: float, params: CTMLMParameters) -> float:
    """Simplified entrainment closure.

    Entrainment is enhanced by cloud-top radiative cooling and cloud fraction.
    This transparent closure is useful for thesis sensitivity experiments.
    """
    inversion_jump = max(params.s_plus - params.s_surface, 1.0)
    cooling_factor = params.delta_F * (0.2 + float(clip_cloud_fraction(C)))
    w_e = params.entrainment_eff * cooling_factor / (params.rho0 * params.cp * inversion_jump)
    return max(w_e, params.min_entrainment)


def decoupling_like_variable(z_b: float) -> float:
    """Simple decoupling-like diagnostic based on boundary-layer depth."""
    return max(0.0, (z_b - 600.0) / 1000.0)


def ctmlm_rhs(t: float, y: np.ndarray, params: CTMLMParameters) -> list[float]:
    """Right-hand side of the simplified cloud-topped mixed-layer model.

    State vector
    ------------
    y[0] : z_b
        Boundary-layer height in m.
    y[1] : s_b
        Mixed-layer thermodynamic state in K-like units.
    y[2] : q_b
        Mixed-layer specific humidity in kg kg-1.
    y[3] : C
        Cloud fraction.
    """
    z_b, s_b, q_b, C = y

    z_b = max(float(z_b), params.min_z_b)
    C = float(clip_cloud_fraction(C))

    shf, lhf = surface_fluxes(s_b, q_b, params)
    w_e = entrainment_velocity(z_b, C, params)

    delta_s = params.s_plus - s_b
    delta_q = params.q_plus - q_b

    dzdt = w_e - params.D * z_b
    dsdt = (w_e * delta_s + shf / (params.rho0 * params.cp) - params.delta_F / (params.rho0 * params.cp)) / z_b
    dqdt = (w_e * delta_q + lhf / (params.rho0 * params.lv)) / z_b

    Lambda = decoupling_like_variable(z_b)
    C_eq = cloud_fraction_from_decoupling(
        Lambda,
        C_min=params.C_min,
        C_max=params.C_max,
        Lambda_t=params.Lambda_t,
        Lambda_s=params.Lambda_s,
    )
    dCdt = (float(C_eq) - C) / params.tau_C

    return [dzdt, dsdt, dqdt, dCdt]


def run_model(
    params: CTMLMParameters | None = None,
    y0: list[float] | tuple[float, float, float, float] | None = None,
    days: float = 300.0,
    max_step: float = 3600.0,
):
    """Run the model and return a SciPy solution object."""
    if params is None:
        params = CTMLMParameters()

    if y0 is None:
        y0 = [700.0, 290.0, 0.008, 0.70]

    t_span = (0.0, float(days) * SECONDS_PER_DAY)

    sol = solve_ivp(
        fun=lambda t, y: ctmlm_rhs(t, y, params),
        t_span=t_span,
        y0=np.asarray(y0, dtype=float),
        method="RK45",
        max_step=max_step,
        rtol=1e-6,
        atol=1e-8,
    )

    return sol


def parameter_dict(params: CTMLMParameters) -> dict:
    """Return model parameters as a dictionary."""
    return asdict(params)
