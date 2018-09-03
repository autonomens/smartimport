import os

SRC_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(SRC_DIR)
DATADIR = os.path.join(PROJECT_DIR, 'data')


try:
    from settings_local import *
except ImportError:
    pass
