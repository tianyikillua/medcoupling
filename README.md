# MEDCoupling

[![PyPi Version](https://img.shields.io/pypi/v/medcoupling.svg?style=flat-square)](https://pypi.org/project/medcoupling)

This repository provides a re-packaging of the [MEDCoupling](https://docs.salome-platform.org/latest/dev/MEDCoupling/developer/index.html) library via `setup.py` and hence installable via `pip`.

Running `python3 setup.py build` will

1. Download the source code of MEDCoupling from [salome-platform.org](http://files.salome-platform.org/Salome/other/medCoupling-9.3.0.tar.gz)
2. Builing the C++ / Python libraries using `cmake` and `swig`
3. Distribute generated files using `setuptools`

### Installation

To install MEDCoupling, you can now simply type
```
pip install -U medcoupling
```

### Usage

To assure that MEDCoupling is well installed, try importing it in your Python
```
import medcoupling  # should not raise error
```

### License

MEDCoupling, and hence this repository are published under [LGPL 2.1](https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License).

### Repository author

Tianyi Li <tianyikillua@gmail.com>
