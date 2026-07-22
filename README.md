<h2 align="center"> <a href="https://mcgs-slam.github.io">MCGS-SLAM: A Multi-Camera SLAM Framework Using Gaussian Splatting for High-Fidelity Mapping</a>
</h2>

<h5 align="center">

[![arXiv](https://img.shields.io/badge/Arxiv-2509.14191-b31b1b.svg?logo=arXiv)](https://arxiv.org/abs/2509.14191) 
[![Home Page](https://img.shields.io/badge/Project-Website-33728E.svg)](https://mcgs-slam.github.io) 
[![ICRA 2026](https://img.shields.io/badge/ICRA-2026-e28353.svg)](https://2026.ieee-icra.org) 

Zhihao Cao, Hanyu Wu, Li Wa Tang, Zizhou Luo, Wei Zhang, Marc Pollefeys, Zihan Zhu*, Martin R. Oswald

*Project Lead
</h5>

<div align="center">
TL;DR: A dense SLAM system that leverages multi-camera input and 3D Gaussian Splatting.
</div>
<br>

<div align="center">
  <img src="figures/teaser.png" alt="teaser" />
</div>
<br>

---

## 📦 Installation

Create a new Conda environment and install dependencies. Our setup assumes:

* Ubuntu 22.04
* PyTorch with CUDA 11.8
* GPU: NVIDIA RTX 3080 Ti (16GB VRAM)

```bash
conda env create -f environment.yaml
conda activate mcgs_slam_v1
conda install -c "nvidia/label/cuda-11.8.0" cuda-nvcc=11.8 cuda-cudart-dev=11.8
conda install -c "nvidia/label/cuda-11.8.0" cuda-toolkit
```

Install additional components:

```bash
export CUDA_HOME=$CONDA_PREFIX
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib:$CUDA_HOME/lib64:$LD_LIBRARY_PATH

export CC=gcc-11
export CXX=g++-11
pip install -r requirement.txt --no-build-isolation
pip install -U openmim
mim install mmengine mmcv
```

Install DROID (CUDA), JDSA (CUDA) and MCBA (CUDA):
```bash
export CC=gcc-11
export CXX=g++-11
python setup.py install
```

### Dev Container (Ampere / CUDA 11.8)

The repository includes a headless VS Code devcontainer that builds the pinned
Python environment, compiles all CUDA extensions, and caches the Metric3D
ViT-small model. It targets Linux/x86-64 systems with an NVIDIA RTX 30-series
GPU (compute capability 8.6).

The host must already have Docker, an NVIDIA driver, and the NVIDIA Container
Toolkit configured. Verify GPU passthrough before opening the repository in a
container:

```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

The devcontainer binds the example sequence from
`/home/nicky/datasets/mcgs-example/garden` to `/datasets/garden` read-only.
Generated results are written to the repository's `output/` directory. After
using **Dev Containers: Reopen in Container**, setup automatically checks the
GPU, compiled extensions, and all five synchronized camera streams.

Run the short validation sequence:

```bash
bash .devcontainer/scripts/run-garden.sh smoke
```

Run all 217 frames:

```bash
bash .devcontainer/scripts/run-garden.sh full
```

The smoke run uses stride 3 and stops after 12 keyframes, writing to
`output/garden-smoke`. The full run uses stride 1 and writes to `output/garden`.
Both commands use the calibration-compatible camera order `front_left`,
`front_center`, `front_right`, `left_center`, `right_center`. Interactive
`--vis` and `--gsvis` display forwarding are not configured in this headless
container.

---

## 📥 Download the Data

```bash
wget https://polybox.ethz.ch/index.php/s/JAJpZb2RJAjd4Y5/download/data.zip
unzip data.zip
```

The sequence we provide here is derived from the [Waymo Open Dataset](https://waymo.com/open/). To avoid copyright issues, we only ship this single sequence as an example, for other sequences, please download them directly from [https://waymo.com/open/](https://waymo.com/open/).

In addition, Multi-Camera Airsim (MC-Airsim) Dataset is available from [https://mcgs-slam.github.io/dataset/](https://mcgs-slam.github.io/dataset/).

---

## 🚀 Run MCGS-SLAM

### Non-visual Mapping Mode

```bash
export seq=data/100613
python demo.py --calib calib/100613.yml \
               --imagedir ${seq}/front ${seq}/front_right ${seq}/front_left ${seq}/front_right \
               --stride 1 \
               --output output/100613
```

### Visual Mapping Mode (with Gaussian Splatting Viewer)

```bash
export seq=data/100613
python demo.py --calib calib/100613.yml \
               --imagedir ${seq}/front ${seq}/front_right ${seq}/front_left ${seq}/front_right \
               --stride 1 \
               --output output/100613 \
               --gsvis
```

### ATE (RMSE)
```bash
evo_ape tum data/100613/gt_poses.txt output/100613/traj_mcgs.txt -as
```

### TSDF Visualization
```bash
python tsdf_integrate.py --result output/100613 --device cpu:0 --per_camera
python vis_tsdf_per_cam.py --result output/100613
```

---

## 🧪 Modes

### 1. **Full Optimization Mode (MCBA + JDSA + Prior Depth)**

This mode uses multi-camera bundle adjustment with joint depth–scale alignment and prior-guided depth initialization.

```bash
export seq=data/100613
python demo.py --calib calib/100613.yml \
                         --imagedir ${seq}/front ${seq}/front_right ${seq}/front_left ${seq}/front_right \
                         --stride 1 \
                         --output output/100613 \
                         --prgbd --jdsa
```

### 2. **MCBA + Prior Depth Only (without JDSA)**

JDSA is disabled. Depth is still initialized via priors (e.g., Metric3D).

```bash
export seq=data/100613
python demo.py --calib calib/100613.yml \
                         --imagedir ${seq}/front ${seq}/front_right ${seq}/front_left ${seq}/front_right \
                         --stride 1 \
                         --output output/100613 \
                         --prgbd
```

### 3. **Minimal Optimization Mode (No Prior, No JDSA)**

A simpler version of our method using only multi-view photometric and geometric consistency.

```bash
export seq=data/100613
python demo.py --calib calib/100613.yml \
                         --imagedir ${seq}/front ${seq}/front_right ${seq}/front_left ${seq}/front_right \
                         --stride 1 \
                         --output output/100613
```

---

## 🛠️ Dependencies

* Python 3.8+
* PyTorch >= 1.13.0 (CUDA 11.8)
* OpenMMLab stack: `mmengine`, `mmcv`
* NumPy, OpenCV, PyYAML, etc. (installed via `environment.yaml`)

---

## 📸 Citation and Acknowledgement

If you find this project useful, please consider citing our paper.

```
@article{cao2025mcgs,
  title={Mcgs-slam: A multi-camera slam framework using gaussian splatting for high-fidelity mapping},
  author={Cao, Zhihao and Wu, Hanyu and Tang, Li Wa and Luo, Zizhou and Zhang, Wei and Pollefeys, Marc and Zhu, Zihan and Oswald, Martin R},
  journal={arXiv preprint arXiv:2509.14191},
  year={2025}
}
```

Parts of the code are adapted or reimplemented based on ideas from [BAMF-SLAM](https://arxiv.org/abs/2306.01173), [Hi-SLAM2](https://arxiv.org/abs/2411.17982), and [3D Gaussian Splatting](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/).
