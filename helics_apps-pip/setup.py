import io
import os
import versioneer

from setuptools import setup

# Get the directory setup.py is located in
setup_py_dir = os.path.abspath(os.path.dirname(__file__))

# Get the README.md contents
README_contents = io.open(os.path.join(setup_py_dir, 'README.md'), encoding="utf-8").read()

setup(
    name='helics_apps',
    version=versioneer.get_version(),
    author='GMLC-TDC',
    author_email='helicsdevelopers@helics.org',
    maintainer='',
    maintainer_email='',
    url="https://github.com/GMLC-TDC/HELICS",
    download_url="https://github.com/GMLC-TDC/HELICS/releases",
    license='BSD',
    keywords='helics co-simulation',
    description='Hierarchical Engine for Large-scale Infrastructure Co-Simulation (HELICS)',
    long_description=README_contents,
    long_description_content_type='text/markdown',
    packages=['helics_apps'],
    package_data={'helics_apps': ['data/*']},
    include_package_data=True,
    cmdclass=versioneer.get_cmdclass(),
    entry_points={
        'console_scripts': [
            'helics_app=helics_apps:helics_app',
            'helics_broker=helics_apps:helics_broker',
            'helics_broker_server=helics_apps:helics_broker_server',
            'helics_player=helics_apps:helics_player',
            'helics_recorder=helics_apps:helics_recorder',
        ]
    },
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: C",
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
    ],
)
