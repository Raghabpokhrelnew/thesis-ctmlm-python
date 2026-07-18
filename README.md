# thesis-ctmlm-python

Python implementation of a simplified cloud-topped mixed-layer model for thesis experiments on subtropical low-cloud variability, subsidence weakening, inversion-related stability, and SST warming.

This repository supports the thesis workflow:

- ERA5 diagnostics for California and Namibia stratocumulus regions
- conceptual experiments for subsidence, SST, wind speed, and inversion strength
- interpretation of the subsidence--inversion--cloud pathway
- a transparent Python model that can be modified step by step during thesis development

## Scientific scope

The model is a compact, thesis-oriented implementation inspired by cloud-topped mixed-layer modelling ideas. It is **not** an official Python port of `ConceptualClimateModels.jl`.

The prognostic variables are:

- `z_b`: boundary-layer height
- `s_b`: mixed-layer thermodynamic state
- `q_b`: mixed-layer specific humidity
- `C`: low-cloud fraction

The central mixed-layer height tendency is:

```text
dz_b/dt = w_e - D z_b
```

where `w_e` is entrainment velocity and `D` is a large-scale subsidence/divergence parameter.

## Installation

```bash
git clone https://github.com/Raghabpokhrelnew/thesis-ctmlm-python.git
cd thesis-ctmlm-python
pip install -e .
```

For development:

```bash
pip install -e .[dev]
pytest
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
  constants.py        Physical constants
  parameters.py       Dataclass for model parameters
  thermodynamics.py   Saturation humidity and cloud diagnostics
  model.py            ODE system and numerical solver
  experiments.py      Standard thesis sensitivity experiments
  diagnostics.py      Response summaries and plotting helpers

examples/
  run_standard_experiments.py

tests/
  test_thermodynamics.py
  test_model.py
```

## Thesis use

This package is intended to support experiments such as:

- isolated subsidence weakening
- isolated SST warming
- wind-speed perturbations
- inversion-strength perturbations
- combined ERA5-guided forcing experiments

The model is intentionally simple so that its assumptions and limitations can be explained clearly in a thesis.

## License

MIT License.
