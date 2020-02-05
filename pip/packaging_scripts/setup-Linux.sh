#!/bin/bash

VERSION=$1

curl -O -L https://github.com/Kitware/CMake/releases/download/v3.16.2/cmake-3.16.2-Linux-x86_64.tar.gz
tar xzf cmake-*.tar.gz && rm cmake-*.tar.gz && mv cmake-* cmake
PATH="${PWD}/cmake/bin:${PATH}"
export PATH

# Install swig, but don't add it to the PATH until the Python 3 interfaces are built
curl -L -o "swig-4.0.1.tar.gz" \
           "https://sourceforge.net/projects/swig/files/swig/swig-4.0.1/swig-4.0.1.tar.gz/download"
tar -zxf "swig-4.0.1.tar.gz"
pushd swig-4.0.1
curl -L -O "https://ftp.pcre.org/pub/pcre/pcre-8.43.tar.gz"
./Tools/pcre-build.sh
./configure --prefix "$HOME/swig-install"
make
make install
popd

# Get HELICS shared library for Linux
curl -O -L "https://github.com/GMLC-TDC/HELICS/releases/download/v${VERSION}/Helics-shared-${VERSION}-Linux-x86_64.tar.gz"
tar xzf Helics-*.tar.gz && rm Helics-*.tar.gz && mv Helics-* helics
CMAKE_PREFIX_PATH="${PWD}/helics"
export CMAKE_PREFIX_PATH

# Checkout the HELICS source tree into the pip folder
git clone -b python-nolink --single-branch https://github.com/GMLC-TDC/HELICS pip/bundled/helics

