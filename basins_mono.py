"""
Basins of AI Alignment: The Adversarial Boundary (Mono Variant)
------------------------------------
Same alignment-landscape model as basins_color.py, rendered in ink-on-paper
style to match ridgelines_mono.py. The two basins are distinguished by
marker shape (circle vs triangle) rather than colour, so the piece reads
correctly even in greyscale print.

Author: Ali Mieyitayo
"""

import numpy as np
import matplotlib.pyplot as plt

SEED = 8021
rng = np.random.default_rng(SEED)


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


def main():
    extent = 2.3
    size = 700
    xs = np.linspace(-extent, extent, size)
    ys = np.linspace(-extent, extent, size)
    X, Y = np.meshgrid(xs, ys)
    Z = potential(X, Y)

    gX, gY = gradient(X, Y)
    U, V = -gX, -gY

    fig, ax = plt.subplots(figsize=(12, 12), dpi=300)
    fig.patch.set_facecolor("#f4ecd8")
    ax.set_facecolor("#f4ecd8")

    levels = np.linspace(Z.min(), np.percentile(Z, 70), 26)
    ax.contour(X, Y, Z, levels=levels, colors="#2b2320", linewidths=0.45, alpha=0.55)

    ax.streamplot(
        X, Y, U, V,
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

    n_probes = 260
    probe_x = rng.normal(0.0, 0.30, n_probes)
    probe_y = rng.normal(0.0, 0.55, n_probes)

    for px, py in zip(probe_x, probe_y):
        fx, fy = descend(px, py)
        landed_aligned = fx < 0
        marker = "o" if landed_aligned else "^"
        ax.plot(px, py, marker=marker, markersize=3.6, color="#2b2320", alpha=0.7, zorder=4)

    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.tight_layout(pad=0)
    plt.savefig("basins_mono.png", facecolor=fig.get_facecolor(),
                bbox_inches="tight", pad_inches=0.15)
    print("Saved basins_mono.png")


if __name__ == "__main__":
    main()