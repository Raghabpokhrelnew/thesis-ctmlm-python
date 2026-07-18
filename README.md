# thesis-ctmlm-python

Python implementation of a simplified cloud-topped mixed-layer model for thesis experiments on subsidence, inversion-related stability, and subtropical low-cloud variability.

This repository supports the thesis workflow:

- ERA5 diagnostics of subtropical stratocumulus regions
- sensitivity experiments for subsidence, SST, wind speed, and inversion strength
- conceptual interpretation of the subsidence-inversion-cloud pathway

## Scientific scope

The package implements a transparent CTMLM-style conceptual model with prognostic variables for:

- boundary-layer height `z_b`
- mixed-layer thermodynamic state `s_b`
- mixed-layer humidity `q_b`
- cloud fraction `C`

The core mixed-layer mechanism is

```text
dz_b/dt = w_e - D z_b
```

where `w_e` is entrainment velocity and `D` is a subsidence or large-scale divergence parameter.

This is **not an official Python port** of `ConceptualClimateModels.jl`. It is an independent thesis implementation inspired by cloud-topped mixed-layer modelling ideas and designed for ERA5-guided sensitivity experiments.

## Installation

```bash
git clone https://github.com/Raghabpokhrelnew/thesis-ctmlm-python.git
cd thesis-ctmlm-python
pip install -e .
```

## Quick start

```python
from thesis_ctmlm import run_standard_experiments

results = run_standard_experiments()
print(results)
```

## Repository structure

```text
src/thesis_ctmlm/
  constants.py        physical constants
  parameters.py       model parameter dataclass
  thermodynamics.py   helper equations
  model.py            ODE system and solver
  experiments.py      standard sensitivity experiments
  diagnostics.py      response summaries and plotting helpers

tests/
  test_thermodynamics.py
```

## Thesis use

This package is intended to support experiments such as:

- isolated subsidence weakening
- isolated SST warming
- wind-speed perturbations
- inversion-strength perturbations
- combined ERA5-guided forcing experiments

The model is intentionally simple so that its assumptions and limitations can be explained clearly in the thesis.

## License

MIT License.