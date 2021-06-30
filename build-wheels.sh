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
echo "Hi"
ls -lrt
cd /src/

#!/bin/bash

#for bindir in /opt/python/*/bin; do
#    "$bindir/pip" wheel /src/ -w wheelhouse/
#done
/opt/python/cp38-cp38/bin/pip wheel /src/ -w wheelhouse/
ls -lrt 
ls -lrt wheelhouse/
for whl in /src/wheelhouse/cassandra_driver-*.whl; do
    auditwheel repair "$whl" -w /src/wheelhouse/
done


