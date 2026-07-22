from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

import os
import os.path as osp
ROOT = osp.dirname(osp.abspath(__file__))


def cuda_arch_flags():
    """Return explicit NVCC flags, optionally narrowed for container builds."""
    configured = os.environ.get("MCGS_CUDA_ARCH_LIST")
    architectures = (
        configured.replace(",", " ").split()
        if configured
        else ["6.0", "6.1", "7.0", "7.5", "8.0", "8.6"]
    )
    return [
        f"-gencode=arch=compute_{arch.replace('.', '')},code=sm_{arch.replace('.', '')}"
        for arch in architectures
    ]


CUDA_ARCH_FLAGS = cuda_arch_flags()

setup(
    name='droid_backends',
    ext_modules=[
        CUDAExtension('droid_backends',
            include_dirs=[osp.join(ROOT, 'thirdparty/eigen')],
            sources=[
                'src/droid.cpp', 
                'src/droid_kernels.cu',
                'src/correlation_kernels.cu',
                'src/altcorr_kernel.cu',
            ],
            extra_compile_args={
                'cxx': ['-O3'],
                'nvcc': ['-O3'] + CUDA_ARCH_FLAGS,
            }),
    ],
    cmdclass={ 'build_ext' : BuildExtension }
)

setup(
    name='lietorch',
    version='0.2',
    description='Lie Groups for PyTorch',
    packages=['lietorch'],
    package_dir={'': 'thirdparty/lietorch'},
    ext_modules=[
        CUDAExtension('lietorch_backends', 
            include_dirs=[
                osp.join(ROOT, 'thirdparty/lietorch/lietorch/include'), 
                osp.join(ROOT, 'thirdparty/eigen')],
            sources=[
                'thirdparty/lietorch/lietorch/src/lietorch.cpp', 
                'thirdparty/lietorch/lietorch/src/lietorch_gpu.cu',
                'thirdparty/lietorch/lietorch/src/lietorch_cpu.cpp'],
            extra_compile_args={
                'cxx': ['-O2'], 
                'nvcc': ['-O2'] + CUDA_ARCH_FLAGS,
            }),
    ],
    cmdclass={ 'build_ext' : BuildExtension }
)
