#!/bin/bash

# Copy everything to home
cp -r /io/* ~/
cd ~/

# Install swig
yum install -y pcre-devel
curl -L https://github.com/swig/swig/archive/refs/tags/rel-4.0.2.tar.gz | tar xz \
&& cd swig-rel-4.0.2 && ./autogen.sh && ./configure --without-alllang && make && make install

# Build wheels for Python 3.7, 3.8, 3.9
cd ~/
for PYVERSION in 7; do
    export PYTHON_ROOT_DIR=/opt/python/cp3${PYVERSION}-cp3${PYVERSION}m
    ${PYTHON_ROOT_DIR}/bin/pip install cmake numpy scipy
    touch ${PYTHON_ROOT_DIR}/lib/libpython3.${PYVERSION}m.so
    export CMAKE_EXE=${PYTHON_ROOT_DIR}/bin/cmake
    ${PYTHON_ROOT_DIR}/bin/python3 setup.py bdist_wheel --plat-name manylinux2014_x86_64
done
for PYVERSION in 8 9; do
    export PYTHON_ROOT_DIR=/opt/python/cp3${PYVERSION}-cp3${PYVERSION}
    ${PYTHON_ROOT_DIR}/bin/pip install cmake numpy scipy
    touch ${PYTHON_ROOT_DIR}/lib/libpython3.${PYVERSION}m.so
    export CMAKE_EXE=${PYTHON_ROOT_DIR}/bin/cmake
    ${PYTHON_ROOT_DIR}/bin/python3 setup.py bdist_wheel --plat-name manylinux2014_x86_64
done

# Copy wheels to /io
mkdir -p /io/dist/
cp ~/dist/* /io/dist/
