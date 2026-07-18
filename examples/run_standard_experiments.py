"""Run standard thesis CTMLM experiments.

Usage:
    python examples/run_standard_experiments.py
"""

from pathlib import Path

from thesis_ctmlm import run_standard_experiments, run_era5_guided_experiments
from thesis_ctmlm.diagnostics import (
    save_results,
    response_summary,
    plot_cloud_response,
    plot_boundary_layer_response,
)


def main() -> None:
    results_dir = Path("results")
    figures_dir = Path("figures")
    results_dir.mkdir(exist_ok=True)
    figures_dir.mkdir(exist_ok=True)

    standard = run_standard_experiments()
    era5 = run_era5_guided_experiments()

    save_results(standard, results_dir / "standard_experiments.csv")
    save_results(era5, results_dir / "era5_guided_experiments.csv")

    print("Standard experiments")
    print(response_summary(standard))
    print("\nERA5-guided experiments")
    print(response_summary(era5))

    plot_cloud_response(standard, figures_dir / "standard_cloud_response.png")
    plot_boundary_layer_response(standard, figures_dir / "standard_boundary_layer_response.png")
    plot_cloud_response(era5, figures_dir / "era5_cloud_response.png")
    plot_boundary_layer_response(era5, figures_dir / "era5_boundary_layer_response.png")


if __name__ == "__main__":
    main()
