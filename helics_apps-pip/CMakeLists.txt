cmake_minimum_required(VERSION 3.15...3.26)
project(HELICS LANGUAGES CXX) # Must be "HELICS" due to its CMake files requiring CMAKE_PROJECT_NAME == PROJECT_NAME in order to build app executables

message(STATUS "--------------------")
message(STATUS "SYSTEM ${CMAKE_SYSTEM}")
message(STATUS "SYSTEM_PROCESSOR ${CMAKE_SYSTEM_PROCESSOR}")
message(STATUS "SYSTEM_VERSION ${CMAKE_SYSTEM_VERSION}")
message(STATUS "SYSTEM_NAME ${CMAKE_SYSTEM_NAME}")
message(STATUS "APPLE ${APPLE}")
message(STATUS "LINUX ${LINUX}")
message(STATUS "UNIX ${UNIX}")
message(STATUS "WIN32 ${WIN32}")
message(STATUS "ENV(TEST_ENV_VAR) $ENV{TEST_ENV_VAR}")

return()
message(STATUS ${SKBUILD_PROJECT_NAME})
message(STATUS ${SKBUILD_PROJECT_VERSION})
message(STATUS ${SKBUILD_PROJECT_VERSION_FULL})
message(STATUS ${SKBUILD_STATE})
message(STATUS ${SKBUILD_PLATLIB_DIR})
message(STATUS ${SKBUILD_DATA_DIR})

include(FetchContent)

# Only fetch source code files if it is building an sdist
if(NOT SKBUILD_STATE STREQUAL "sdist")
    set(FETCHCONTENT_FULLY_DISCONNECTED ON)
endif()

# NOTE: SKBUILD_PROJECT_VERSION strips some of the extra Python version components out, like postN and devM
# The setuptools_scm "no-guess-dev" version_scheme works well, since that leaves it with just the HELICS version
set(CMAKE_CXX_STANDARD 17)
set(HELICS_DISABLE_GIT_OPERATIONS ON)
set(HELICS_ZMQ_SUBPROJECT ON)
set(HELICS_ZMQ_FORCE_SUBPROJECT ON)
set(HELICS_ENABLE_ZMQ_CORE OFF)
set(HELICS_DISABLE_BOOST ON) # TODO: headers are just needed to compile, maybe tell users to have it when building from source
set(HELICS_BUILD_APP_LIBRARY ON)
set(HELICS_BUILD_APP_EXECUTABLES ON)
FetchContent_Declare(
    helics
    URL https://github.com/GMLC-TDC/HELICS/releases/download/v${SKBUILD_PROJECT_VERSION}/Helics-v${SKBUILD_PROJECT_VERSION}-source.tar.gz
    SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/helics-src
)

# For making the sdist, only need to download the source code
if(SKBUILD_STATE STREQUAL "sdist")
    if(NOT helics_POPULATED)
        FetchContent_Populate(HELICS)
        message(STATUS "Populated HELICS")
    endif()
elseif(SKBUILD_STATE STREQUAL "wheel")
    add_library(helicsCpp98_ide INTERFACE)
    FetchContent_MakeAvailable(helics)
endif()
message(STATUS ${helics_POPULATED})
message(STATUS ${helics_SOURCE_DIR})
message(STATUS ${helics_BINARY_DIR})


# HELICS_SOURCE = os.path.join(setup_py_dir, "./_source")
# HELICS_VERSION = versioneer.get_version()
# HELICS_VERSION = re.findall(r"(?:(\d+\.(?:\d+\.)*\d+))", HELICS_VERSION)[0]
# HELICS_INSTALL = os.path.join(setup_py_dir, "./helics_apps/data")
# DOWNLOAD_URL = "https://github.com/GMLC-TDC/HELICS/releases/download/v{version}/Helics-v{version}-source.tar.gz".format(version=HELICS_VERSION)