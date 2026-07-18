"""Thesis CTMLM Python package.

A compact cloud-topped mixed-layer model for ERA5-guided thesis experiments.
"""

from .parameters import CTMLMParameters
from .model import ctmlm_rhs, run_model
from .experiments import (
    final_state,
    run_experiment,
    run_standard_experiments,
    run_era5_guided_experiments,
)

__all__ = [
    "CTMLMParameters",
    "ctmlm_rhs",
    "run_model",
    "final_state",
    "run_experiment",
    "run_standard_experiments",
    "run_era5_guided_experiments",
]
