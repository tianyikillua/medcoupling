import glob
import os
import platform
import shutil
import subprocess
import sys
import tarfile
from urllib.request import urlretrieve

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py as _build_py

# Metadata
__author__ = "Tianyi Li"
__email__ = "tianyikillua@gmail.com"
__copyright__ = "Copyright (c) 2019-2021 {} <{}>".format(__author__, __email__)
__license__ = "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)"
__version__ = "9.7.0r1"
__status__ = "Development Status :: 4 - Beta"

basedir = os.path.dirname(os.path.realpath(__file__))


def download_build_medcoupling():

    # Source file to download
    MEDCOUPLING_SRC = (
        "http://files.salome-platform.org/Salome/other/medCoupling-9.7.0.tar.gz"
    )

    # Environment variables
    CMAKE_EXE = os.environ.get("CMAKE_EXE", shutil.which("cmake"))
    SWIG_ROOT_DIR = os.environ.get("SWIG_ROOT_DIR")
    PYTHON_ROOT_DIR = os.environ.get("PYTHON_ROOT_DIR")
    BUILD_TYPE = os.environ.get("BUILD_TYPE")
    if BUILD_TYPE is None:
        BUILD_TYPE = "Release"

    version_medcoupling = MEDCOUPLING_SRC.partition("medCoupling-")[2].partition(
        ".tar"
    )[0]
    sourcedir = os.path.join(basedir, f"medCoupling-{version_medcoupling}")
    configdir = os.path.join(basedir, f"configuration-{version_medcoupling}")
    installdir = os.path.join(basedir, "medcoupling")

    def check_cmake():
        if not CMAKE_EXE:
            print(
                "cmake executable not found. Set CMAKE_EXE environment or update your path"
            )
            sys.exit(1)

    def check_swig():
        if not shutil.which("swig"):
            print(
                "swig executable not found. Set SWIG_ROOT_DIR environment or update your path"
            )
            sys.exit(1)

    def check_python():
        if not shutil.which("python") and not shutil.which("python3"):
            print(
                "python or python3 executable not found. Set PYTHON_ROOT_DIR environment or update your path"
            )
            sys.exit(1)
        else:
            try:
                import numpy
            except ImportError:
                print("numpy is not installed")
                sys.exit(1)

    # Preliminary checks
    check_cmake()
    check_swig()
    check_python()

    # Cleanup previous built files
    for f in glob.glob(os.path.join(installdir, "*")):
        if "__init__.py" not in f:
            os.remove(f)

    # Download source files
    print(f"Downloading {MEDCOUPLING_SRC}...")
    filename, _ = urlretrieve(MEDCOUPLING_SRC)
    src = tarfile.open(filename)
    print(f"Extracting...")
    src.extractall()

    # Building
    builddir = os.path.join(sourcedir, "build")
    os.makedirs(builddir, exist_ok=True)

    cmake_args = [
        CMAKE_EXE,
        sourcedir,
        "-DCMAKE_INSTALL_PREFIX=install",
        "-DMEDCOUPLING_MICROMED=ON",
        "-DMEDCOUPLING_BUILD_DOC=OFF",
        "-DMEDCOUPLING_ENABLE_PARTITIONER=OFF",
        "-DMEDCOUPLING_BUILD_TESTS=OFF",
        "-DMEDCOUPLING_ENABLE_RENUMBER=OFF",
        "-DMEDCOUPLING_WITH_FILE_EXAMPLES=OFF",
        "-DCMAKE_BUILD_TYPE=" + BUILD_TYPE,
    ]
    if PYTHON_ROOT_DIR is not None:
        cmake_args += [f"-DPYTHON_ROOT_DIR={PYTHON_ROOT_DIR}"]
    if SWIG_ROOT_DIR is not None:
        cmake_args += [f"-DSWIG_ROOT_DIR={SWIG_ROOT_DIR}"]
    if platform.system() != "Windows":
        cmake_args += ["-DMEDCOUPLING_BUILD_STATIC=ON"]

    env = os.environ.copy()
    env["CONFIGURATION_ROOT_DIR"] = configdir
    subprocess.check_call(cmake_args, cwd=builddir, env=env)

    cmake_build_args = [
        CMAKE_EXE,
        "--build",
        ".",
        "--config",
        BUILD_TYPE,
        "--target",
        "install",
    ]
    subprocess.check_call(cmake_build_args, cwd=builddir, env=env)

    print("Copying C++/Python libary files...")
    lib_dir = os.path.join(builddir, "install", "lib")
    for f in glob.glob(os.path.join(lib_dir, "*.dll")):
        shutil.move(f, installdir)
    for f in glob.glob(os.path.join(lib_dir, "*.so")):
        shutil.move(f, installdir)

    python_dir = os.path.join(lib_dir, "python3.*", "site-packages")
    for f in glob.glob(os.path.join(python_dir, "*.py*")):
        shutil.move(f, installdir)
    for f in glob.glob(os.path.join(python_dir, "*.so")):
        shutil.move(f, installdir)

    # Remove source files
    shutil.rmtree(configdir, ignore_errors=True)
    shutil.rmtree(sourcedir, ignore_errors=True)


class build_py(_build_py):
    def run(self):
        download_build_medcoupling()
        _build_py.run(self)


# Force platform-specific bdist
# https://stackoverflow.com/questions/45150304/how-to-force-a-python-wheel-to-be-platform-specific-when-building-it
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False


except ImportError:
    bdist_wheel = None


setup(
    name="medcoupling",
    version=__version__,
    packages=find_packages(),
    package_data={"": ["*.dll", "*.so", "*.pyd"]},
    url="https://github.com/tianyikillua/medcoupling",
    author=__author__,
    author_email=__email__,
    install_requires=["numpy"],
    description="Python repackaging of the MEDCoupling library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license=__license__,
    classifiers=[
        __license__,
        __status__,
        # See <https://pypi.org/classifiers/> for all classifiers.
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    cmdclass={"build_py": build_py, "bdist_wheel": bdist_wheel},
)
