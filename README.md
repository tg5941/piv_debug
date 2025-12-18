# piv_debug

Minimal reproducible example to investigate **low GPU utilization** when using the **GPU-accelerated OpenPIV** (`openpiv.gpu`) library.

---

## Repository Contents

piv_debug/

├── README.md

├── environment.yml # Conda environment (CUDA, PyCUDA, OpenPIV GPU)

└── PIV_utils_tg.py # GPU PIV test and batch utilities

## Environment Setup

Create and activate the Conda environment:

```bash
conda env create -f environment.yml
conda activate PIV_test
```
Requirements:

CUDA-capable NVIDIA GPU

Working NVIDIA drivers (nvidia-smi)

Expected Data Structure

Input images must be PNGs arranged as:
```bash
<im_loc>/<file_name>/
├── Left/
│   ├── frame_0001.png
│   ├── frame_0002.png
│   └── ...
└── Right/
    ├── frame_0001.png
    ├── frame_0002.png
    └── ...
```
Left and Right folders must contain the same number of frames.

## Output

Results are written to:

<gen_loc>/Shifts/<file_name>/*.mat


Each file contains:

Displacement fields (shiftx, shifty)

PIV grid (X, Y)

Valid mask

Minimal Example
params = dict(
    window_size=32,
    overlap=16,
    search_area_size=64,
    dt=1.0,
)

PIV_single_test(
    batch_n=10,
    gen_loc="./output/",
    im_loc="./images/",
    file_name="experiment_001",
    params=params
)

Example ipbyn file should run directly without modifying anything.
