"""Reusable artwork generation helpers for algorithmic art pieces."""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

SEED_RIDGE = 4217
SEED_BASIN = 8021


def orientation_field(X, Y, core, delta, weight=0.5):
    core_angle = np.arctan2(Y - core[1], X - core[0])
    delta_angle = np.arctan2(Y - delta[1], X - delta[0])
    return (2.0 * core_angle - delta_angle) * weight


def build_orientation_field(X, Y, singularities):
    theta_total = np.zeros_like(X)
    for core, delta, w in singularities:
        theta_total += orientation_field(X, Y, core, delta, w)
    return theta_total


def _ridgelines_singularity_parameters():
    return [
        ((-0.62, 0.42), (-1.05, -1.55), 0.55),
        ((0.68, -0.35), (1.15, 1.05), 0.45),
    ]


def _make_ridgelines_field(size=1000, extent=3.2):
    x = np.linspace(-extent, extent, size)
    y = np.linspace(-extent, extent, size)
    X, Y = np.meshgrid(x, y)
    singularities = _ridgelines_singularity_parameters()
    theta = build_orientation_field(X, Y, singularities)
    ripple = 0.05 * np.sin(2.3 * X + 0.7) * np.cos(1.9 * Y - 0.4)
    theta = theta + ripple
    return X, Y, theta, singularities


def create_ridgelines(variant, output_path, size=1000, extent=3.2, dpi=300):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    X, Y, theta, singularities = _make_ridgelines_field(size=size, extent=extent)
    U = np.cos(theta)
    V = np.sin(theta)

    fig, ax = plt.subplots(figsize=(12, 12), dpi=dpi)
    if variant == "mono":
        fig.patch.set_facecolor("#f4ecd8")
        ax.set_facecolor("#f4ecd8")
        color = "#2b2320"
        linewidth = 0.55
        strm = ax.streamplot(
            X,
            Y,
            U,
            V,
            density=3.6,
            linewidth=linewidth,
            color=color,
            arrowstyle="-",
            integration_direction="both",
            broken_streamlines=True,
        )
        strm.lines.set_alpha(0.85)
    else:
        fig.patch.set_facecolor("#0d0d12")
        ax.set_facecolor("#0d0d12")
        colour_field = np.mod(theta, np.pi)
        strm = ax.streamplot(
            X,
            Y,
            U,
            V,
            density=3.6,
            linewidth=0.9,
            color=colour_field,
            cmap="twilight_shifted",
            arrowstyle="-",
            integration_direction="both",
            broken_streamlines=True,
        )
        strm.lines.set_alpha(0.92)

    for core, delta, _ in singularities:
        if variant == "mono":
            ax.plot(*core, marker="o", markersize=4, color="#8a2e2e", alpha=0.65)
            ax.plot(*delta, marker="^", markersize=4, color="#2e4a8a", alpha=0.65)
        else:
            ax.plot(*core, marker="o", markersize=6, color="#ffdd55", alpha=0.9, zorder=5)
            ax.plot(*delta, marker="^", markersize=6, color="#55e0ff", alpha=0.9, zorder=5)

    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return output_path


def potential(x, y):
    well = (x**2 - 1.15) ** 2 + 0.9 * y**2
    asymmetry = 0.22 * x * (y**2) - 0.10 * x
    tilt = 0.05 * x
    return well + asymmetry + tilt


def gradient(x, y, h=1e-4):
    dVdx = (potential(x + h, y) - potential(x - h, y)) / (2 * h)
    dVdy = (potential(x, y + h) - potential(x, y - h)) / (2 * h)
    return dVdx, dVdy


def descend(x0, y0, steps=4000, lr=0.01):
    x, y = x0, y0
    for _ in range(steps):
        gx, gy = gradient(x, y)
        x -= lr * gx
        y -= lr * gy
    return x, y


def create_basins(variant, output_path, extent=2.3, size=700, dpi=300):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED_BASIN)
    xs = np.linspace(-extent, extent, size)
    ys = np.linspace(-extent, extent, size)
    X, Y = np.meshgrid(xs, ys)
    Z = potential(X, Y)
    gX, gY = gradient(X, Y)
    U, V = -gX, -gY

    fig, ax = plt.subplots(figsize=(12, 12), dpi=dpi)
    if variant == "mono":
        fig.patch.set_facecolor("#f4ecd8")
        ax.set_facecolor("#f4ecd8")
        levels = np.linspace(Z.min(), np.percentile(Z, 70), 26)
        ax.contour(X, Y, Z, levels=levels, colors="#2b2320", linewidths=0.45, alpha=0.55)
        ax.streamplot(
            X,
            Y,
            U,
            V,
            density=1.6,
            linewidth=0.5,
            color="#5a5044",
            arrowstyle="-",
            broken_streamlines=True,
        )
        ax.plot(-1.15, 0, marker="o", markersize=11, color="#2b2320", zorder=5)
        ax.text(-1.15, -0.22, "aligned", ha="center", fontsize=11, color="#2b2320", family="monospace")
        ax.plot(1.0, 0, marker="^", markersize=11, color="#2b2320", zorder=5)
        ax.text(1.0, -0.22, "misaligned", ha="center", fontsize=11, color="#2b2320", family="monospace")
    else:
        fig.patch.set_facecolor("#0d0d12")
        ax.set_facecolor("#0d0d12")
        levels = np.linspace(Z.min(), np.percentile(Z, 78), 40)
        ax.contourf(X, Y, Z, levels=levels, cmap="plasma", alpha=0.9)
        ax.contour(X, Y, Z, levels=levels, colors="#ffffff", linewidths=0.25, alpha=0.25)
        stream = ax.streamplot(
            X,
            Y,
            U,
            V,
            density=1.6,
            linewidth=0.6,
            color="#ffffff",
            arrowstyle="-",
            broken_streamlines=True,
        )
        stream.lines.set_alpha(0.35)
        ax.plot(
            -1.15,
            0,
            marker="o",
            markersize=13,
            color="#39ff88",
            markeredgecolor="#0d0d12",
            markeredgewidth=1.5,
            zorder=5,
        )
        ax.text(
            -1.15,
            -0.24,
            "aligned",
            ha="center",
            fontsize=12,
            color="#39ff88",
            family="monospace",
            weight="bold",
        )
        ax.plot(
            1.0,
            0,
            marker="o",
            markersize=11,
            color="#ff4d4d",
            markeredgecolor="#0d0d12",
            markeredgewidth=1.5,
            zorder=5,
        )
        ax.text(
            1.0,
            -0.24,
            "misaligned",
            ha="center",
            fontsize=12,
            color="#ff4d4d",
            family="monospace",
            weight="bold",
        )

    n_probes = 260
    probe_x = rng.normal(0.0, 0.30, n_probes)
    probe_y = rng.normal(0.0, 0.55, n_probes)

    for px, py in zip(probe_x, probe_y):
        fx, fy = descend(px, py)
        landed_aligned = fx < 0
        if variant == "mono":
            marker = "o" if landed_aligned else "^"
            ax.plot(px, py, marker=marker, markersize=3.6, color="#2b2320", alpha=0.7, zorder=4)
        else:
            colour = "#39ff88" if landed_aligned else "#ff4d4d"
            ax.plot(
                px,
                py,
                marker="o",
                markersize=4.2,
                color=colour,
                markeredgecolor="#0d0d12",
                markeredgewidth=0.4,
                alpha=0.95,
                zorder=4,
            )

    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return output_path


def create_piece(piece_name, output_path=None, **kwargs):
    mapping = {
        "ridgelines_mono": (create_ridgelines, "mono", "ridgelines_mono.png"),
        "ridgelines_color": (create_ridgelines, "color", "ridgelines_color.png"),
        "basins_mono": (create_basins, "mono", "basins_mono.png"),
        "basins_color": (create_basins, "color", "basins_color.png"),
    }
    if piece_name not in mapping:
        raise ValueError(f"Unknown piece '{piece_name}'")
    fn, variant, default_name = mapping[piece_name]
    if output_path is None:
        output_path = Path(default_name)
    return fn(variant, output_path, **kwargs)