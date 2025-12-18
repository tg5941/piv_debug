PIV Debug: GPU Acceleration Benchmarking
This repository is created to replicate low GPU utilization issues when using the GPU-accelerated Open-PIV library. It contains a structured pipeline for processing image pairs and saving the resulting displacement vectors as .mat files.

🚀 Quick Start: Environment Replication
To replicate the working environment, ensure you have Conda installed. This project requires NVIDIA GPU support and CUDA-compatible libraries.

1. Create the Environment
Use the provided environment.yml to build the PIV_test environment:

Bash

conda env create -f environment.yml
2. Activate the Environment
Bash

conda activate PIV_test


📂 Project Structure
environment.yml: Full Conda environment specification including nvidia channels, pycuda, and openpiv.

PIV_utils_tg.py: The core logic containing:

PIV_single_test: A diagnostic function to run an initial PIV pass and visualize the results.

worker: A multi-GPU ready function designed to process batches of images and save outputs.

list_png_files: A utility to handle natural sorting of image sequences.

🛠 How the Code Works
1. Initial Setup (PIV_single_test)
This function acts as the "Pre-flight check." It:

Loads the first pair of images from /Left and /Right directories.

Creates a PIV_mask based on zero-pixel intensity.

Calls process.gpu_piv to perform the initial cross-correlation.

Visualization: It generates a 3-panel plot showing the Left image, Right image, and the calculated velocity magnitude to ensure the parameters are correct before batch processing.

2. Batch Processing (worker)
The worker function is designed for high-throughput processing:

GPU Targeting: Uses os.environ["CUDA_VISIBLE_DEVICES"] to pin the process to a specific GPU ID.

Memory Efficiency: Pre-allocates NumPy arrays (u1, v1, etc.) to store displacement vectors for a full batch.

Batch Loop: Iterates through the image sequence, reads pairs using imageio, and computes PIV shifts on the GPU.

Storage: Saves results in .mat format, compatible with MATLAB or Python's scipy.io.

📥 Input Requirements
The code expects the following directory structure:

Plaintext

data/
└── your_experiment_name/
    ├── Left/
    │   ├── img_001.png
    │   └── ...
    └── Right/
        ├── img_001.png
        └── ...
