# MEDCoupling

[![PyPi Version](https://img.shields.io/pypi/v/medcoupling-pypi.svg?style=flat-square)](https://pypi.org/project/medcoupling-pypi)

This repository provides a Python repackaging of the latest version (9.3.0) of the [MEDCoupling](https://docs.salome-platform.org/latest/dev/MEDCoupling/developer/index.html) library via a Python file `setup.py` and hence installable via `pip`.

Running `python3 setup.py build` will

1. Download the source code of MEDCoupling from [salome-platform.org](http://files.salome-platform.org/Salome/other/medCoupling-9.3.0.tar.gz)
2. Builing the C++ / Python libraries using `cmake` and `swig`
3. Distribute generated files using `setuptools`

### Installation

To install MEDCoupling, you can now simply type
```
pip install -U medcoupling-pypi
```

Binary wheels are available for 64-bit Windows (`amd64`) and Linux-like platforms (`x86_64`). In accordance with the [release notes of SALOME 9.3.0](https://files.salome-platform.org/Salome/Salome9.3.0/SALOME_9_3_0_Release_Notes.pdf), the wheels are only built with Python 3.6. Sadly macOS is not supported (consult developers of MEDCoupling).

### Usage

To assure that MEDCoupling is well installed, try importing it in your Python
```
import medcoupling  # should not raise error
```

### Uploading to PyPI

To upload binary wheels to PyPI, type
```
# on Windows
python setup.py bdist_wheel --plat-name win_amd64

# on Linux
python3 setup.py bdist_wheel --plat-name manylinux1_x86_64

python[3] -m twine upload dist/*
```

### License

MEDCoupling, and hence this repository are published under [LGPL 2.1](https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License).

### Repository author

Tianyi Li <tianyikillua@gmail.com>
