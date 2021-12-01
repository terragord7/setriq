from __future__ import print_function
import sys
if sys.version_info < (3,):
    print('Python 2 has reached end-of-life and is not supported by setriq.')
    sys.exit(-1)
if sys.platform == 'win32' and sys.maxsize.bit_length() == 31:
    print('32-bit Windows Python runtime is not supported. Please switch to 64-bit Python.')
    sys.exit(-1)

import logging
import pathlib
import re
import traceback
from glob import glob

from pybind11.setup_helpers import ParallelCompile, Pybind11Extension
from setuptools import setup, find_packages

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s - %(asctime)s.%(msecs)03d - %(levelname)s - %(module)s.%(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

dirname = pathlib.Path(__file__).parent
long_description = (dirname / 'README.md').read_text()

try:
    changelog = (dirname / 'CHANGELOG.md').read_text()
    __version__, *_ = re.findall(r"\[([0-9.]+)]", changelog)
except (FileNotFoundError, ValueError) as ex:
    __version__ = '0.1.0'
    logging.error(ex)
    logging.error(traceback.print_exc())
    logging.warning(f'Unable to get semantic release version. Setting version to {__version__}.')

PROJECT_NAME = 'setriq'
SOURCE_DIR = 'src'

ParallelCompile("NPY_NUM_BUILD_JOBS").install()

extensions = [
    Pybind11Extension(
        f'{PROJECT_NAME}._C',
        sources=sorted(glob(f'{SOURCE_DIR}/{PROJECT_NAME}/_C/**/*.cpp', recursive=True)),
        cxx_std=14,
        define_macros=[('VERSION_INFO', __version__)],
        include_dirs=['include/setriq'],
        extra_compile_args=['-O3']
    ),
]

setup(
    name=PROJECT_NAME,
    version=__version__,
    description='Python package written in C++ for pairwise distance computation for sequences.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='benjamin-tenmann',
    author_email='b.tenmann@me.com',
    url='https://github.com/BenTenmann/setriq',
    ext_modules=extensions,
    license='MIT',
    python_requires='>=3.7,<3.10',
    package_dir={f'{PROJECT_NAME}': f'{SOURCE_DIR}/{PROJECT_NAME}'},
    packages=find_packages(where=f'{SOURCE_DIR}', exclude=['tests', 'scripts']),
    package_data={f'{PROJECT_NAME}': sorted(glob(f'data/*.json'))},
    include_package_data=True
)
