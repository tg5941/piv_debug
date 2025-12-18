# PIV_debug: GPU Acceleration Benchmarking

This repository provides a framework to replicate and investigate low GPU utilization issues when using the **Open-PIV** library with GPU acceleration. It is designed to process high-frequency image sequences (Left/Right stereo pairs) and benchmark the performance of the GPU-based cross-correlation.

## 📋 Table of Contents
* [Environment Setup](#-environment-setup)
* [Code Overview](#-code-overview)
* [Data Structure](#-data-structure)
* [Key Bottlenecks Under Investigation](#-key-bottlenecks-under-investigation)

---

## 🚀 Environment Setup

This project requires an NVIDIA GPU and a specific Conda environment to handle `pycuda` and `openpiv` dependencies.

### 1. Replicate the Environment
Run the following command in your terminal to create the environment from the provided `environment.yml`:
```bash
conda env create -f environment.yml
