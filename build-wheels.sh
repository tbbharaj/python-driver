#!/bin/bash
#set -e -u -x
#echo ${PLAT}
#echo ${PYTHON}
# Create binary wheels
#/opt/python/${PYTHON}/bin/pip wheel /src/ -w wheelhouse/

#ls -lrt /src/
#ls -lrt wheelhouse/

# Normalize resulting binaries to a common format
#for whl in wheelhouse/cassandra_driver-*.whl; do
#    auditwheel repair "$whl" -w /src/wheelhouse/
#done




#!/bin/bash
set -e -u -x
ls -lrt /opt/
ls -lrt /opt/python/${PYTHON}/
cd /src/

#for bindir in /opt/python/*/bin; do
#    "$bindir/pip" wheel /src/ -w wheelhouse/
#done
/opt/python/${PYTHON}/bin/pip wheel /src/ -w wheelhouse/
ls -lrt wheelhouse/
for whl in wheelhouse/cassandra_driver-*.whl; do
    auditwheel repair "$whl" -w wheelhouse/
done


