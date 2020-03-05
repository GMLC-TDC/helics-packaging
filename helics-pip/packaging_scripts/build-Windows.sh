#!/bin/bash

WINARCH=$1

export CMAKE_PREFIX_PATH

# Convert the Windows-style tool cache path set by GitHub Actions to a Unix-style path
bash_runner_tool_cache=$(echo "/${RUNNER_TOOL_CACHE}" | sed -e 's/\\/\//g' -e 's/://')

# Compile wheels
pushd helics-pip || exit $?
OLD_PATH=$PATH
for PYDIR in "${bash_runner_tool_cache}"/Python/3*/"${WINARCH}"; do
  pythonLocation="${PYDIR}"
  export pythonLocation
  echo "Building wheel using Python at ${pythonLocation}"
  PATH="${PYDIR}/Scripts:${PYDIR}:$OLD_PATH"
  export PATH
  "$PYDIR/python" -m pip install --upgrade pip
  "$PYDIR/python" -m pip install setuptools wheel
  "$PYDIR/python" setup.py bdist_wheel --dist-dir=../wheelhouse
done

choco install -y swig || exit $?
OLD_PATH="$HOME/swig-install/bin:$OLD_PATH"
for PYDIR in "${bash_runner_tool_cache}"/Python/2*/"${WINARCH}"; do
  pythonLocation="${PYDIR}"
  export pythonLocation
  echo "Building wheel using Python at ${pythonLocation}"
  PATH="${PYDIR}/Scripts:${PYDIR}:$OLD_PATH"
  export PATH
  "$PYDIR/python" -m pip install --upgrade pip
  "$PYDIR/python" -m pip install setuptools wheel
  "$PYDIR/python" setup.py bdist_wheel --dist-dir=../wheelhouse
done
popd || exit $?
