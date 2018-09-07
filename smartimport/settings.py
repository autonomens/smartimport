import os

SRC_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)
DATADIR = os.path.join(PROJECT_DIR, 'data')
MODEL_PATH = os.path.join('.', 'model.pkl')
ID_TO_TYPE_MAP_PATH = os.path.join('.', 'learned_classes.json')

# algo key is mandatory, others are passed to constructor.
STR2FEATURES_CONF = {
    "algo": 'OnePixelByLetter',
    "max_length": 50
}

try:
    from settings_local import *
except ImportError:
    pass
