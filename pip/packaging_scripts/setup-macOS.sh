#!/bin/bash

VERSION=$1

# Install HELICS shared library for macOS
curl -O -L https://github.com/nightlark/HELICS/releases/latest/download/Helics-shared-${VERSION}-macOS-x86_64.tar.gz
tar xzf Helics-*.tar.gz && rm Helics-*.tar.gz && mv Helics-* helics

# Checkout the HELICS source tree into the pip folder
git clone -b python-nolink --single-branch https://github.com/GMLC-TDC/HELICS pip/bundled/helics

# Set the CMAKE_PREFIX_PATH environment variable in GitHub Actions
echo "::set-env name=CMAKE_PREFIX_PATH::${PWD}/helics"

# Set the DYLD_LIBRARY_PATH in GitHub Actions so delocate can fix up the wheels
echo "::set-env name=DYLD_LIBRARY_PATH::$PWD/helics/lib:$PWD/helics/lib64:$DYLD_LIBRARY_PATH"

