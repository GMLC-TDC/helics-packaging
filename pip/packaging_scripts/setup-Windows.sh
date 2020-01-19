#!/bin/bash

VERSION=$1
WINARCH=$2

# Install HELICS shared library for Windows
curl -O -L https://github.com/nightlark/HELICS/releases/download/v${VERSION}/Helics-shared-${VERSION}-${WINARCH}.tar.gz
tar xzf Helics-*.tar.gz && rm Helics-*.tar.gz && mv Helics-* helics

# Checkout the HELICS source tree into the pip folder
git clone -b python-nolink --single-branch https://github.com/GMLC-TDC/HELICS pip/bundled/helics
mkdir wheelhouse

# Set the CMAKE_PREFIX_PATH environment variable in GitHub Actions
echo "::set-env name=CMAKE_PREFIX_PATH::${PWD}/helics"

