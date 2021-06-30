#!/bin/bash
set -e -u -x
echo "Hi"
ls -lrt
cd /src/

#!/bin/bash

#for bindir in /opt/python/*/bin; do
#    "$bindir/pip" wheel /src/ -w wheelhouse/
#done
/opt/python/cp38-cp38/bin/pip wheel /src/ -w wheelhouse/
ls -lrt wheelhouse/
for whl in /src/wheelhouse/cassandra_driver-*.whl; do
    auditwheel repair "$whl" -w /src/wheelhouse/
done


# Create binary wheels
#/opt/python/${PYTHON}/bin/python3 setup.py bdist_wheel

# Normalize resulting binaries to a common format
#for whl in dist/*.whl; do
#    auditwheel repair $whl --plat "${PLAT}" -w wheelhouse
#done

if [ `uname -m` = 'aarch64' ]; then
	/opt/python/cp38-cp38/bin/pip3 install /src/cassandra_driver-*.whl
#else
#	/opt/python/cp39-cp39/bin/pip3.9 install /io/*-manylinux2014_x86_64.whl
fi
