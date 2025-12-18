# PIV_debug: GPU Acceleration & Utilization Benchmarking

This repository provides a framework to replicate and investigate low GPU utilization issues when using the **Open-PIV** library with GPU acceleration. It is designed to process high-frequency image sequences (Stereo Left/Right pairs) and benchmark the performance of the GPU-based cross-correlation engine.

---

## 📋 Table of Contents
1. [Environment Setup](#1-environment-setup)
2. [Data Structure](#2-data-structure)
3. [Code Logic & Architecture](#3-code-logic--architecture)
4. [Debugging Goals](#4-debugging-goals)
5. [Replication Steps](#5-replication-steps)

---

## 1. Environment Setup

This project requires an NVIDIA GPU and specific CUDA-compatible libraries. The provided `environment.yml` contains all necessary dependencies, including `pycuda`, `openpiv`, and `numba`.

### Replicate the Environment
Run the following commands in your terminal:
```bash
# Create the environment from the yml file
conda env create -f environment.yml

# Activate the environment
conda activate PIV_test

2. Data Structure
To ensure the scripts run correctly, organize your local image data as follows. The code utilizes natsort to ensure frames are processed in the correct chronological order.

Plaintext

piv_debug/
├── PIV_utils_tg.py      # Core processing utilities
├── environment.yml      # Conda environment definition
├── README.md            # Project documentation
└── [your_data_folder]/
    └── [experiment_name]/
        ├── Left/        # Sequence of .png files for the left camera
        └── Right/       # Sequence of .png files for the right camera
3. Code Logic & Architecture
The logic in PIV_utils_tg.py is structured to facilitate both rapid testing and heavy batch processing:

Diagnostic Phase (PIV_single_test)
This function serves as a pre-processing check:

Masking: It automatically generates a PIV mask where pixel intensity is zero in either image.

GPU Pass: Runs an initial process.gpu_piv to establish a baseline.

Verification: Generates a matplotlib figure showing the source pair and the resulting velocity magnitude ($ \sqrt{D1^2 + D2^2} $) to verify the search window parameters.

Batch Processing Phase (worker)
A multi-GPU ready function designed for high-throughput benchmarking:

GPU Isolation: Dynamically sets CUDA_VISIBLE_DEVICES based on the assigned gpu_id.

Array Pre-allocation: Pre-allocates large NumPy arrays (u1, v1, u2, v2) based on the D1.shape to prevent memory fragmentation during the loop.

Output Handling: Consolidates all displacement vectors and the mask into a dictionary for export as a single .mat file per batch.
