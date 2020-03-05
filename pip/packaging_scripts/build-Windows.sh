#!/bin/bash

WINARCH=$1

export CMAKE_PREFIX_PATH

# Compile wheels
pushd pip || exit $?
OLD_PATH=$PATH
for PYDIR in "${RUNNER_TOOL_CACHE}"/Python/3*/"${WINARCH}"; do
  pythonLocation="${PYDIR}"
  echo "Building wheel using Python at ${pythonLocation}"
  PATH="${PYDIR}/Scripts:${PYDIR}:$OLD_PATH"
  export PATH
  "$PYDIR/python" -m pip install --upgrade pip
  "$PYDIR/python" -m pip install setuptools wheel
  "$PYDIR/python" setup.py bdist_wheel --dist-dir=../wheelhouse
done

choco install -y swig || exit $?
OLD_PATH="$HOME/swig-install/bin:$OLD_PATH"
for PYDIR in "${RUNNER_TOOL_CACHE}"/Python/2*/"${WINARCH}"; do
  pythonLocation="${PYDIR}"
  echo "Building wheel using Python at ${pythonLocation}"
  PATH="${PYDIR}/Scripts:${PYDIR}:$OLD_PATH"
  export PATH
  "$PYDIR/python" -m pip install --upgrade pip
  "$PYDIR/python" -m pip install setuptools wheel
  "$PYDIR/python" setup.py bdist_wheel --dist-dir=../wheelhouse
done
popd || exit $?
