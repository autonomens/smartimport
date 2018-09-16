
import pickle

import numpy as np
import pandas as pd

from smartimport import settings, str2features, types

_model = None


def get_model():
    """ Load and return model """

    global _model
    if not _model:
        with open(settings.MODEL_PATH, "rb") as f:
            # load model
            _model = pickle.load(f)

    return _model


def get_algo():
    """ get algo to compute features """
    conf = dict(settings.STR2FEATURES_CONF)
    return getattr(str2features, conf.pop("algo"))(**conf)


def guess(data):
    """ Guess data type for each value """

    algo = get_algo()
    model = get_model()

    # convert data in features
    nb_rows, nb_cols = data.shape
    features = np.empty((nb_cols * nb_rows, algo.nb_features()))

    idx = 0
    for _, row in data.iterrows():
        for value in row:
            features[idx] = algo.convert(str(value))
            idx = idx + 1

    # Actually predict
    predicted = model.predict(features)

    # Reshape prediction with the original shape
    predicted = pd.DataFrame(predicted.reshape(*data.shape), columns=data.columns)

    # Force emtpy values to unknown type
    predicted[data.isna()] = 0

    headers = [{"orig_name": h} for h in data.columns]

    unique_count = data.nunique()

    for header in headers:
        h = header["orig_name"]
        header["name"] = h.capitalize().strip()
        count = pd.value_counts(predicted[:][h])
        valid_count = data[:][h].dropna().shape[0]

        # Sum of dectecd types by column
        header["all_predictions"] = [
            (types.get_type_by_label(pred), k) for pred, k in count.items()
        ]

        if (
            header["all_predictions"][0][0].label != 0
            or len(header["all_predictions"]) <= 1
        ):
            # More frequent type
            header["guessed_type"] = header["all_predictions"][0][0]
        else:
            header["guessed_type"] = header["all_predictions"][1][0]

        # Unique values count to detect enum
        header["unique_count"] = int(
            unique_count[h]
        )  # Convert to int to allow json serialization

        # enum probability
        # TODO here it's possible to have a finer analysis
        if valid_count > (
            data.shape[0] * 0.05
        ):  # can't decide if less than 5% of valid values
            header["enum_score"] = 1 - header["unique_count"] / valid_count
        else:
            header["enum_score"] = 0

        # Add type data
        header["guessed_type"].populate_header(header, data)
        # Add guessed name
        header["guessed_name"] = header["guessed_type"].header_name

    return headers
