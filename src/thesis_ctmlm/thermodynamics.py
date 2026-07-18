"""Thermodynamic helper functions for the thesis CTMLM model."""

from __future__ import annotations

import numpy as np


def saturation_vapor_pressure(T: float | np.ndarray) -> float | np.ndarray:
    """Approximate saturation vapor pressure over liquid water.

    Parameters
    ----------
    T : float or ndarray
        Temperature in K.

    Returns
    -------
    float or ndarray
        Saturation vapor pressure in Pa.
    """
    T_c = np.asarray(T) - 273.15
    return 611.2 * np.exp((17.67 * T_c) / (T_c + 243.5))


def saturation_specific_humidity(T: float | np.ndarray, p: float = 100000.0) -> float | np.ndarray:
    """Approximate saturation specific humidity over liquid water.

    Parameters
    ----------
    T : float or ndarray
        Temperature in K.
    p : float
        Pressure in Pa.

    Returns
    -------
    float or ndarray
        Saturation specific humidity in kg kg-1.
    """
    e_s = saturation_vapor_pressure(T)
    return 0.622 * e_s / (p - 0.378 * e_s)


def cloud_fraction_from_decoupling(
    Lambda: float | np.ndarray,
    C_min: float = 0.0,
    C_max: float = 0.9,
    Lambda_t: float = 0.23,
    Lambda_s: float = 0.50,
) -> float | np.ndarray:
    """Smooth diagnostic cloud-fraction relation.

    Smaller values of the decoupling-like variable are interpreted as more
    stratocumulus-favorable. Larger values reduce cloud fraction.
    """
    Lambda = np.asarray(Lambda)
    return C_min + 0.5 * (C_max - C_min) * (1.0 + np.tanh((Lambda_t - Lambda) / Lambda_s))


def clip_cloud_fraction(C: float | np.ndarray) -> float | np.ndarray:
    """Limit cloud fraction to the physical interval [0, 1]."""
    return np.clip(C, 0.0, 1.0)
