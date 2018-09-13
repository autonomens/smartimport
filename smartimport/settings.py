import os

SRC_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)
DATADIR = "."
MODEL_PATH = os.path.join(DATADIR, "model.pkl")
ID_TO_TYPE_MAP_PATH = os.path.join(DATADIR, "learned_classes.json")
TRAINING_DATA_PATH = os.path.join(DATADIR, "training_data.csv")

# algo key is mandatory, others are passed to constructor.
STR2FEATURES_CONF = {"algo": "OnePixelByLetter", "max_length": 50}

TRAINING_MODEL = (
    "sklearn.ensemble.ExtraTreesClassifier",
    dict(n_jobs=-1, verbose=0),
)

try:
    from settings_local import * # noqa
except ImportError:
    pass
