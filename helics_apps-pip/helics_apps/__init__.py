import os
import subprocess
import sys

try:
    from ._version import __version__, __version_tuple__
except ModuleNotFoundError:
    __version__ = ""
    __version_tuple__ = ()

DATA = os.path.join(os.path.dirname(__file__), 'data')

BIN_DIR = os.path.join(DATA, 'bin')

def _program(name, args):
    return subprocess.call([os.path.join(BIN_DIR, name)] + args)

def helics_app():
    raise SystemExit(_program('helics_app', sys.argv[1:]))

def helics_broker():
    raise SystemExit(_program('helics_broker', sys.argv[1:]))

def helics_broker_server():
    raise SystemExit(_program('helics_broker_server', sys.argv[1:]))

def helics_player():
    raise SystemExit(_program('helics_player', sys.argv[1:]))

def helics_recorder():
    raise SystemExit(_program('helics_recorder', sys.argv[1:]))

def helics_connector():
    raise SystemExit(_program('helics_connector', sys.argv[1:]))


