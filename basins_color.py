"""
Basins of AI Alignment: The Adversarial Boundary
--------------------
Generative art piece exploring the intersection of cybersecurity and AI
alignment.

Concept:
An AI system's behaviour can be modelled as a trajectory descending a
"potential landscape" toward one of several stable outcomes (attractors).
Here, two basins exist: a wide, deep "aligned" basin, and a narrower,
shallower "misaligned" basin sitting right beside it, separated by a
saddle ridge.

Trajectories starting from almost the same point can end up in entirely
different basins depending on which side of the ridge they begin on - a
direct visual analogy for how a small adversarial perturbation (the
red-teaming intuition from cybersecurity) can tip an otherwise well-behaved
system across an alignment boundary it never appeared close to from a
single trajectory alone.

A field of "probe" points is scattered along the ridge itself - these are
colour-coded by which basin they ultimately fall into, visualising exactly
the kind of boundary-mapping a security red team performs when searching
for the smallest perturbation that flips a system's behaviour.

The piece is fully deterministic: same seed, same landscape, same probes,
every run.

Author: Ali Mieyitayo
"""

import numpy as np
import matplotlib.pyplot as plt

# ---- Reproducibility ------------------------------------------------
SEED = 8021
rng = np.random.default_rng(SEED)


# ---- The potential landscape -----------------------------------------
def potential(x, y):
    """
    Asymmetric double-well potential. The 'aligned' basin (left, around
    x = -1.15) is wider and deeper. The 'misaligned' basin (right, around
    x = 1.0) is narrower and shallower - still a stable resting state, just
    a worse one, exactly like a misaligned-but-locally-stable policy.
    """
    well = (x**2 - 1.15) ** 2 + 0.9 * y**2
    asymmetry = 0.22 * x * (y**2) - 0.10 * x
    tilt = 0.05 * x  # slight overall tilt favouring the aligned basin
    return well + asymmetry + tilt


def gradient(x, y, h=1e-4):
    """Numerical gradient of the potential, used for steepest-descent flow."""
    dVdx = (potential(x + h, y) - potential(x - h, y)) / (2 * h)
    dVdy = (potential(x, y + h) - potential(x, y - h)) / (2 * h)
    return dVdx, dVdy


def descend(x0, y0, steps=4000, lr=0.01):
    """Runs steepest descent from (x0, y0) and returns the final basin."""
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
    U, V = -gX, -gY  # steepest-descent direction (flow toward minima)

    fig, ax = plt.subplots(figsize=(12, 12), dpi=300)
    fig.patch.set_facecolor("#0d0d12")
    ax.set_facecolor("#0d0d12")

    # Filled topographic surface using a vivid diverging colormap so the
    # landscape itself carries most of the colour, not just the probes.
    levels = np.linspace(Z.min(), np.percentile(Z, 78), 40)
    contourf = ax.contourf(X, Y, Z, levels=levels, cmap="plasma", alpha=0.9)
    ax.contour(X, Y, Z, levels=levels, colors="#ffffff", linewidths=0.25, alpha=0.25)

    # Flow field showing how trajectories descend toward each basin
    ax.streamplot(
        X, Y, U, V,
        density=1.6,
        linewidth=0.6,
        color="#ffffff",
        arrowstyle="-",
        broken_streamlines=True,
    ).lines.set_alpha(0.35)

    # Mark the two attractors
    ax.plot(-1.15, 0, marker="o", markersize=13, color="#39ff88",
             markeredgecolor="#0d0d12", markeredgewidth=1.5, zorder=5)
    ax.text(-1.15, -0.24, "aligned", ha="center", fontsize=12, color="#39ff88", family="monospace", weight="bold")
    ax.plot(1.0, 0, marker="o", markersize=11, color="#ff4d4d",
             markeredgecolor="#0d0d12", markeredgewidth=1.5, zorder=5)
    ax.text(1.0, -0.24, "misaligned", ha="center", fontsize=12, color="#ff4d4d", family="monospace", weight="bold")

    # ---- Probe field: red-team sampling along the ridge -----------------
    # Sample points near the saddle ridge (roughly x in [-0.3, 0.3]),
    # run each through steepest descent, and colour by which basin it
    # actually lands in. This is the visual heart of the piece: two probes
    # that start almost identically can resolve to opposite outcomes.
    n_probes = 260
    probe_x = rng.normal(0.0, 0.30, n_probes)
    probe_y = rng.normal(0.0, 0.55, n_probes)

    for px, py in zip(probe_x, probe_y):
        fx, fy = descend(px, py)
        landed_aligned = fx < 0
        colour = "#39ff88" if landed_aligned else "#ff4d4d"
        ax.plot(px, py, marker="o", markersize=4.2, color=colour,
                 markeredgecolor="#0d0d12", markeredgewidth=0.4, alpha=0.95, zorder=4)

    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.tight_layout(pad=0)
    plt.savefig("basins_color.png", facecolor=fig.get_facecolor(),
                bbox_inches="tight", pad_inches=0.15)
    print("Saved basins_color.png")


if __name__ == "__main__":
    main()