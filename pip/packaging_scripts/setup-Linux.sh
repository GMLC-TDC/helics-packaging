#!/bin/bash

VERSION=$1

curl -O -L https://github.com/Kitware/CMake/releases/download/v3.16.2/cmake-3.16.2-Linux-x86_64.tar.gz
tar xzf cmake-*.tar.gz && rm cmake-*.tar.gz && mv cmake-* cmake
PATH="${PWD}/cmake/bin:${PATH}"
export PATH

# Get HELICS shared library for Linux
curl -O -L https://github.com/nightlark/HELICS/releases/latest/download/Helics-shared-${VERSION}-Linux-x86_64.tar.gz
tar xzf Helics-*.tar.gz && rm Helics-*.tar.gz && mv Helics-* helics
CMAKE_PREFIX_PATH="${PWD}/helics"
export CMAKE_PREFIX_PATH

# Checkout the HELICS source tree into the pip folder
git clone -b python-nolink --single-branch https://github.com/GMLC-TDC/HELICS pip/bundled/helics

