#!/bin/bash
set -e -u -x

# Create binary wheels
/opt/python/${PYTHON}/bin/pip wheel /src/ -w wheelhouse/

ls -lrt /src/
ls -lrt wheelhouse/

# Normalize resulting binaries to a common format
for whl in wheelhouse/cassandra_driver-*.whl; do
    auditwheel repair "$whl" -w /src/wheelhouse/
done
