# MEDCoupling

[![pypi](https://img.shields.io/pypi/v/medcoupling.svg?style=flat-square)](https://pypi.org/project/medcoupling)

This repository provides a Python repackaging of the latest version (9.3.0) of the [MEDCoupling](https://docs.salome-platform.org/latest/dev/MEDCoupling/developer/index.html) library via a Python file `setup.py` and hence installable via `pip`.

### Building from source

Running `python setup.py install` or `pip install .` will

1. Download the source code of MEDCoupling from [salome-platform.org](http://files.salome-platform.org/Salome/other/medCoupling-9.3.0.tar.gz)
2. Build the C++ / Python libraries using `cmake` and `swig`
3. Distribute and install generated files using `setuptools`

The building process has been tested under Windows 10 with Visual Studio 2019 and under Ubuntu 18.04 with gcc 7.4.

### Installation from PyPI

To install MEDCoupling, you can also simply use the binary wheels available on PyPI
```
pip install -U medcoupling
```

Binary wheels are available for 64-bit Windows (`win_amd64`) and Linux-like platforms (`manylinux1_x86_64`) and are built with Python 3.6 and 3.7. Sadly macOS is not supported (consult developers of MEDCoupling).

To assure that MEDCoupling is well installed, try importing it in your Python
```
import medcoupling  # should not raise error
```

### Versioning

The version of this package (on PyPI) follows that of MEDCoupling. For MEDCoupling 9.3.0 for instance, we use
```
v9.3.0r1, v9.3.0r2, ...
```
to designate all PyPI releases based on MEDCoupling 9.3.0. The suffix `r[x]` is included (abusively, since according to PEP 440 it is for post releases) for possible bug fixes coming from this package.

### Uploading to PyPI

To upload source and binary wheels to PyPI, type
```
# Source
python setup.py sdist

# Binary on Windows
python setup.py bdist_wheel --plat-name win_amd64

# Binary on Linux
python setup.py bdist_wheel --plat-name manylinux1_x86_64

# Upload to PyPI
python -m twine upload dist/*
```

### License

MEDCoupling, and hence this repository are published under [LGPL 2.1](https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License).

### Repository author

Tianyi Li <tianyikillua@gmail.com>
