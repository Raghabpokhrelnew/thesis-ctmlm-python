"""Model parameter definitions."""

from dataclasses import dataclass, replace

from .constants import CP, LV, RHO0


@dataclass(frozen=True)
class CTMLMParameters:
    """Parameters for a simplified cloud-topped mixed-layer model.

    This is a thesis implementation inspired by cloud-topped mixed-layer
    modelling ideas. It is not an official translation of ConceptualClimateModels.jl.

    Units
    -----
    D : s-1
        Large-scale subsidence/divergence parameter.
    U : m s-1
        Near-surface wind speed used in bulk fluxes.
    SST : K
        Sea-surface temperature.
    s_plus, s_surface : K-like
        Free-tropospheric and surface thermodynamic states.
    q_plus, q_surface : kg kg-1
        Free-tropospheric and surface specific humidity.
    delta_F : W m-2
        Cloud-top radiative cooling magnitude.
    tau_C : s
        Cloud-fraction adjustment timescale.
    """

    D: float = 4.0e-6
    U: float = 7.0
    SST: float = 289.0

    s_plus: float = 301.0
    q_plus: float = 0.002
    s_surface: float = 289.0
    q_surface: float = 0.010

    delta_F: float = 70.0
    rho0: float = RHO0
    cp: float = CP
    lv: float = LV

    ce: float = 1.0e-3
    entrainment_eff: float = 0.20

    tau_C: float = 2.0 * 86400.0
    C_min: float = 0.0
    C_max: float = 0.90

    Lambda_t: float = 0.23
    Lambda_s: float = 0.50

    min_z_b: float = 50.0
    min_entrainment: float = 1.0e-5

    def with_updates(self, **kwargs) -> "CTMLMParameters":
        """Return a new parameter object with selected fields changed."""
        return replace(self, **kwargs)
