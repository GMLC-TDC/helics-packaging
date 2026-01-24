# helics-packaging
Assorted things for releasing HELICS in package repositories

## Workflows
This has the workflows needed to begin the process of updating packages for new HELICS releases.

- [Update HELICS Packages](https://github.com/GMLC-TDC/helics-packaging/actions/workflows/update-helics.yml): bump the HELICS version number for pyhelics and matHELICS (and eventually trigger the below package updates as well)
- [Spack Package Update](https://github.com/GMLC-TDC/helics-packaging/actions/workflows/update-spack-package.yml): creates a PR to update the HELICS [spack package](https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/helics/package.py)
- [MINGW Package Update](https://github.com/GMLC-TDC/helics-packaging/actions/workflows/update-mingw-package.yml): creates a PR to update the HELICS [MINGW package](https://github.com/msys2/MINGW-packages/blob/master/mingw-w64-helics/PKGBUILD)

- [HELICS Version Update](https://github.com/GMLC-TDC/helics-packaging/actions/workflows/helics_version_update.yml): automatically called from the [release build workflow in GMLC-TDC/HELICS](https://github.com/GMLC-TDC/HELICS/blob/main/.github/workflows/release-build.yml)

Errors running this workflows are likely either a temporary network connectivity issue, regex that needs updating, issue sync'ing the GMLC-TDC mirror of an upstream package repository, or a change to the GitHub API for creating PRs.

## helics_apps-pip (no longer used)
This previously built Python wheels that had the HELICS apps (helics_app, helics_broker, etc), but those are now included as part of [pyhelics](https://github.com/GMLC-TDC/pyhelics) and are obtained when doing a `pip install helics`.
 
A Python pip package with the HELICS apps (helics_app, helics_broker, etc) - [PyPI](https://pypi.org/project/helics-apps), [TestPyPI](https://test.pypi.org/project/helics-apps)

## helics-pip (no longer used)
This previously built the Python wheels for PyPI using swig. It has been replaced by [pyhelics](https://github.com/GMLC-TDC/pyhelics)

A Python pip package with the HELICS python interface - [PyPI](https://pypi.org/project/helics), [TestPyPI](https://test.pypi.org/project/helics)

