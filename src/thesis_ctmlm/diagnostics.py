"""Diagnostics and plotting helpers for CTMLM experiment output."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def response_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return compact response columns for thesis interpretation."""
    keep = [
        col
        for col in [
            "region",
            "experiment_name",
            "D",
            "SST",
            "U",
            "z_b",
            "C",
            "dz_b",
            "dC",
            "success",
        ]
        if col in df.columns
    ]
    return df[keep].copy()


def save_results(df: pd.DataFrame, path: str | Path) -> Path:
    """Save a DataFrame to CSV and return the path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def plot_cloud_response(df: pd.DataFrame, path: str | Path | None = None):
    """Plot cloud-fraction response relative to control."""
    plot_df = df[df["experiment_name"] != "Control"].copy()

    if "region" in plot_df.columns:
        pivot = plot_df.pivot(index="experiment_name", columns="region", values="dC")
        ax = pivot.plot(kind="barh", figsize=(9, 6))
    else:
        ax = plot_df.set_index("experiment_name")["dC"].plot(kind="barh", figsize=(8, 5))

    ax.axvline(0, linestyle="--", linewidth=1)
    ax.set_xlabel("Change in cloud fraction")
    ax.set_title("Cloud-fraction response")
    plt.tight_layout()

    if path is not None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(path, dpi=300)

    return ax


def plot_boundary_layer_response(df: pd.DataFrame, path: str | Path | None = None):
    """Plot boundary-layer-height response relative to control."""
    plot_df = df[df["experiment_name"] != "Control"].copy()

    if "region" in plot_df.columns:
        pivot = plot_df.pivot(index="experiment_name", columns="region", values="dz_b")
        ax = pivot.plot(kind="barh", figsize=(9, 6))
    else:
        ax = plot_df.set_index("experiment_name")["dz_b"].plot(kind="barh", figsize=(8, 5))

    ax.axvline(0, linestyle="--", linewidth=1)
    ax.set_xlabel("Change in boundary-layer height (m)")
    ax.set_title("Boundary-layer-height response")
    plt.tight_layout()

    if path is not None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(path, dpi=300)

    return ax
