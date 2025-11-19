# src/symrock/plots.py
"""
Plotting utilities for the 1D vertical rocket mechanics lab.

These helpers are intentionally simple and rely only on Matplotlib.
"""

from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


def plot_altitude(
    t: np.ndarray,
    h: np.ndarray,
    title: str = "Vertical trajectory",
    xlabel: str = "Time [s]",
    ylabel: str = "Altitude [m]",
):
    """
    Plot altitude vs time.

    Returns
    -------
    matplotlib.axes.Axes
        The axis with the plotted data.
    """
    fig, ax = plt.subplots()
    ax.plot(t, h)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    return ax


def plot_velocity(
    t: np.ndarray,
    v: np.ndarray,
    title: str = "Velocity profile",
    xlabel: str = "Time [s]",
    ylabel: str = "Vertical velocity [m/s]",
):
    """
    Plot vertical velocity vs time.

    Returns
    -------
    matplotlib.axes.Axes
        The axis with the plotted data.
    """
    fig, ax = plt.subplots()
    ax.plot(t, v)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    return ax


def plot_altitude_and_velocity(
    t: np.ndarray,
    h: np.ndarray,
    v: np.ndarray,
    title: str = "Vertical rocket trajectory",
    xlabel: str = "Time [s]",
    altitude_label: str = "Altitude [m]",
    velocity_label: str = "Vertical velocity [m/s]",
    legend_loc: str = "best",
):
    """
    Plot altitude and vertical velocity on the same figure
    (two curves with a shared time axis).

    Returns
    -------
    matplotlib.axes.Axes
        The axis with the plotted data.
    """
    fig, ax = plt.subplots()
    ax.plot(t, h, label=altitude_label)
    ax.plot(t, v, label=velocity_label)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Value")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.legend(loc=legend_loc)
    return ax
