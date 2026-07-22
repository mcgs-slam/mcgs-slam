FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG MINIFORGE_VERSION=24.3.0-0
ARG MINIFORGE_SHA256=23367676b610de826f50f7ddc91139a816d4b59bd4c69cc9b6082d9b2e7fe8a3
ARG METRIC3D_REVISION=eb5b6fac0dc155e4e52f576e304fbf11655ff339
ARG METRIC3D_MODEL_REVISION=80d2d1410afb4b23cd9d18c6be9144483d4b70b6
ARG METRIC3D_MODEL_SHA256=b34b2a2be9148054991cef7e417930e1320602ba7bc503b0ee4e7888543728f6

ENV CONDA_DIR=/opt/conda \
    CUDA_HOME=/usr/local/cuda \
    CC=gcc-11 \
    CXX=g++-11 \
    TORCH_CUDA_ARCH_LIST=8.6 \
    TORCH_HOME=/opt/torch-cache \
    MPLBACKEND=Agg \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash-completion \
        build-essential \
        ca-certificates \
        curl \
        gcc-11 \
        g++-11 \
        git \
        libegl1 \
        libgl1 \
        libglib2.0-0 \
        libgomp1 \
        libsm6 \
        libx11-6 \
        libxext6 \
        libxrender1 \
        ninja-build \
        sudo \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o /tmp/miniforge.sh \
        "https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-x86_64.sh" \
    && echo "${MINIFORGE_SHA256}  /tmp/miniforge.sh" | sha256sum --check --strict \
    && bash /tmp/miniforge.sh -b -p "${CONDA_DIR}" \
    && rm /tmp/miniforge.sh

ENV PATH=/opt/conda/envs/mcgs/bin:/opt/conda/bin:/usr/local/cuda/bin:${PATH} \
    LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

COPY .devcontainer/environment.yml /tmp/environment.yml
RUN conda env create --file /tmp/environment.yml \
    && conda clean --all --yes \
    && rm /tmp/environment.yml

COPY .devcontainer/requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-build-isolation --requirement /tmp/requirements.txt \
    && rm /tmp/requirements.txt

ENV MCGS_CUDA_ARCH_LIST=8.6

WORKDIR /tmp/mcgs-slam
COPY setup.py ./setup.py
COPY src ./src
COPY thirdparty ./thirdparty
RUN python -m pip install --no-build-isolation ./thirdparty/simple-knn \
    && python -m pip install --no-build-isolation ./thirdparty/diff-gaussian-rasterization \
    && python setup.py install \
    && cd / \
    && rm -rf /tmp/mcgs-slam

# Seed Torch Hub with immutable Metric3D source and weights. The application uses
# the standard yvanyin_metric3d_main cache key, so it remains offline at runtime.
RUN mkdir -p "${TORCH_HOME}/hub/yvanyin_metric3d_main" "${TORCH_HOME}/hub/checkpoints" \
    && curl -fsSL \
        "https://github.com/YvanYin/Metric3D/archive/${METRIC3D_REVISION}.tar.gz" \
        | tar -xz --strip-components=1 -C "${TORCH_HOME}/hub/yvanyin_metric3d_main" \
    && curl -fsSL -o "${TORCH_HOME}/hub/checkpoints/metric_depth_vit_small_800k.pth" \
        "https://huggingface.co/JUGGHM/Metric3D/resolve/${METRIC3D_MODEL_REVISION}/metric_depth_vit_small_800k.pth" \
    && echo "${METRIC3D_MODEL_SHA256}  ${TORCH_HOME}/hub/checkpoints/metric_depth_vit_small_800k.pth" \
        | sha256sum --check --strict

RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash vscode \
    && echo "vscode ALL=(root) NOPASSWD:ALL" >/etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode \
    && chown -R vscode:vscode "${TORCH_HOME}"

USER vscode
WORKDIR /workspaces/mcgs-slam
