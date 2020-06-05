import platform

if platform.system() != "Windows":
    from .helics import *
else:
    try:
        from .helics import *
    except ImportError as e:
        # Python 3 has exception chaining: raise ImportError("Custom message") from e
        # If Python 2 support is dropped, use that instead.
        if 'DLL load failed' in str(e):
            raise ImportError(str(e) + "\nSUGGESTED FIX: Install the latest Visual C++ Redistributable for Visual Studio 2019. See https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads for links.")
        else:
            raise ImportError(e)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
