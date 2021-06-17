docker run --rm -v `pwd`:/io quay.io/pypa/manylinux2014_aarch64
ls -lrt
ls wheelhouse/

for bindir in /opt/python/*/bin; do
    "$bindir/pip" wheel ./ -w wheelhouse/
done

for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w ./wheelhouse/
done
