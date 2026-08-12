# Basins of AI Alignment: The Adversarial Boundary — PyCon Greece 2026

Deterministic generative artwork modeling an asymmetric double‑well landscape.
Mono and colour variants show contour/flow fields and probe points that settle into aligned vs misaligned minima.

## Files

- basins_mono.py — ink‑on‑aged‑paper rendering; markers distinguish basins
- basins_color.py — full‑colour rendering with plasma colormap and neon attractors
- requirements.txt — pinned dependencies (numpy, matplotlib)

## Requirements

- Python 3.9+ recommended
- numpy==2.4.4
- matplotlib==3.10.8

Install:

```bash
pip install -r requirements.txt
```

## Run

```bash
python3 basins_mono.py
python3 basins_color.py
```

Each script writes a 12×12 inch PNG (300 DPI by default → 3600×3600 px) to the current directory.

## Determinism

- Fixed seed: 8021. Re‑running produces identical images.
- No external assets or fonts required.

## Concept

An asymmetric double‑well potential defines two attractors: a wide, deep “aligned” basin and a narrower “misaligned” basin separated by a saddle ridge. Streamlines visualize descent; 260 probes near the ridge reveal adversarial flips.

## Notes

- Changing library versions, DPI, or figure parameters may alter results.
- Tested with the pinned dependencies above.

## Author

Eyitayo Alimi (Ali Mieyitayo). © 2026.