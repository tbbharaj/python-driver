#!/bin/bash
set -e -u -x

cd /src/

# Create binary wheels
/opt/python/${PYTHON}/bin/python3 setup.py bdist_wheel

# Normalize resulting binaries to a common format
for whl in dist/*.whl; do
    auditwheel repair $whl --plat "${PLAT}" -w wheelhouse
done

if [ `uname -m` = 'aarch64' ]; then
	/opt/python/${PYTHON}/bin/pip3 install /io/*-manylinux2014_aarch64.whl
#else
#	/opt/python/cp39-cp39/bin/pip3.9 install /io/*-manylinux2014_x86_64.whl
fi
