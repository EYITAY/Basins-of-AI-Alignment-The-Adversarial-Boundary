# Basins of AI Alignment: The Adversarial Boundary 

Deterministic generative artwork modelling an asymmetric double‑well landscape.
Mono and colour variants show contour/flow fields and probe points that settle into aligned vs misaligned minima.

## CyberSecurity + AI Alignment Inspiration

This piece grew out of a career-long habit of treating failure as a boundary to be mapped rather than an anomaly to be patched, after 15+ years in adversarial security, threat modelling, red-teaming, and vulnerability assessment. I've come to see AI alignment the same way: not as a fixed property a system either has or doesn't, but as a landscape with stable and unstable regions, the way a network has hardened paths and exploitable ones. Here, an asymmetric double-well potential defines two attractors, a wide, deep "aligned" basin and a narrower "misaligned" basin sitting right beside it, separated by a saddle ridge. Two starting points that look nearly identical can lead to opposite outcomes depending only on which side of that ridge they begin on. The same intuition behind a red team's search for the smallest input that flips a system's behavior. A field of 260 probes is scattered along the ridge and colour-coded by where each one lands, turning that boundary-mapping instinct into a visual artifact. The piece is fully deterministic — same seed, same landscape, same probes, every run.

## Files

- basins_mono.py: ink‑on‑aged‑paper rendering; markers distinguish basins
- basins_color.py: full‑colour rendering with plasma colormap and neon attractors
- requirements.txt: pinned dependencies (numpy, matplotlib)

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

Eyitayo Alimi — [www.alimieyitayo.com](https://www.alimieyitayo.com). © 2026.

## License

Code and artwork © Eyitayo Alimi — [www.alimieyitayo.com](https://www.alimieyitayo.com). Provided for review as part of a
PyCon Greece 2026 submission; contact the author for reuse permissions.
