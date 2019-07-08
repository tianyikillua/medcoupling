yum install -y pcre-devel
curl -L https://github.com/swig/swig/archive/rel-4.0.0.tar.gz | tar xz \
&& cd swig-rel-4.0.0 && ./autogen.sh && ./configure --without-alllang && make && make install

for PYVERSION in 6 7; do
    export PYTHON_ROOT_DIR=/opt/python/cp3${PYVERSION}-cp3${PYVERSION}m
    ${PYTHON_ROOT_DIR}/bin/pip install cmake numpy scipy
    touch ${PYTHON_ROOT_DIR}/lib/libpython3.${PYVERSION}m.so
    export CMAKE_EXE=${PYTHON_ROOT_DIR}/bin/cmake
    ${PYTHON_ROOT_DIR}/bin/python3 /io/setup.py bdist_wheel --plat-name manylinux2010_x86_64
done

${PYTHON_ROOT_DIR}/bin/python3 /io/setup.py sdist
