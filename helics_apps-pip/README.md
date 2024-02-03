# HELICS Apps
[HELICS](https://github.com/GMLC-TDC/HELICS) is a cross-platform co-simulation framework that enables multiple
simulation tools to exchange data and stay synchronized in time to create larger simulations. This is a set of
binary wheels for macOS, Windows, and Linux for installing the collection of HELICS apps utilities. If you want
the Python interface for writing HELICS programs in Python, see the [helics](https://pypi.org/project/helics/)
pip package.

## Installation
At minimum for the Linux binary wheels to work properly, [pip 19.0 is required](https://packaging.python.org/specifications/platform-compatibility-tags/#manylinux-compatibility-support).
Regardless of your platform, you should probably upgrade pip with `python -m pip install --upgrade` to make
sure the right binary package is found. If you aren't on a supported platform, you will need to compile
the HELICS apps from source or check if your system package manager has a copy of them.

After upgrading pip, running `python -m pip install helics-apps` should fetch a binary wheel if one is available for your platform.

### Binary distributions
This package provides pre-compiled binary wheels for the following operating systems

* Linux 64-bit (manylinux2010 compatible -- glibc 2.12+, most popular distributions released since May 2010)
* macOS Universal2 -- compatible with 10.9+ for Intel macs and 11+ for Apple Silicon macs
* Windows 32/64-bit

### Source distributions
An attempt has been made at providing a source distribution that will compile HELICS from source. Although minimal
support can be provided (e.g. you will need to troubleshoot issues yourself), PRs fixing issues are welcome.

Certain features may not be available when building from source, including the ZeroMQ core and any features that
rely on Boost (such as the interprocess core or web server).

If for some reason using a binary wheel is not an option but a source wheel is and you want to replicate the way the
supported binary wheels are built, set the `CIBUILDWHEEL` environment variable to tell the binary wheel build to
create a wheel from a pre-built HELICS release. Note that you *must* have an internet connection when installing
for this to work, and that it will *only work on glibc x86_64 Linux, 32/64-bit Windows, and macOS systems.

## Release
HELICS is distributed under the terms of the BSD-3 clause license. All new
contributions must be made under this license. [LICENSE](LICENSE)

SPDX-License-Identifier: BSD-3-Clause
