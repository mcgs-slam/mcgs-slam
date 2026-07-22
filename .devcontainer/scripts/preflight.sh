#!/usr/bin/env bash
set -euo pipefail

if ! command -v nvidia-smi >/dev/null 2>&1; then
    echo "nvidia-smi is unavailable. Check the host NVIDIA driver and Container Toolkit." >&2
    exit 1
fi

nvidia-smi --query-gpu=name,compute_cap,memory.total,driver_version --format=csv,noheader

python - <<'PY'
import sys

import torch

if not torch.cuda.is_available():
    raise SystemExit("PyTorch cannot access CUDA inside the container")
if torch.version.cuda != "11.8":
    raise SystemExit(f"Expected PyTorch CUDA 11.8, got {torch.version.cuda}")

sys.path.insert(0, "mcgs_slam")
import droid_backends  # noqa: F401
import lietorch  # noqa: F401
from diff_gaussian_rasterization import GaussianRasterizer  # noqa: F401
from simple_knn._C import distCUDA2  # noqa: F401

major, minor = torch.cuda.get_device_capability(0)
if (major, minor) != (8, 6):
    raise SystemExit(
        f"This image targets Ampere sm_86, but GPU 0 reports sm_{major}{minor}"
    )

print(f"PyTorch {torch.__version__}; CUDA {torch.version.cuda}; GPU {torch.cuda.get_device_name(0)}")
print("MCGS-SLAM CUDA extension imports: OK")
PY
