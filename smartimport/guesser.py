
import pickle
import numpy as np
import pandas as pd
from smartimport import settings, str2features, types


def predict(data, model, algo):
    """
    :param stream: stream to analyze
    :param model: machine learning trained model to analyse data
    :param algo: algorithm to convert original data to features
    :return: a prediction for each column of each row
    """

    # convert data in features
    nb_rows = data.shape[0]
    nb_cols = data.shape[1]
    features = np.empty((nb_cols * nb_rows, algo.nb_features()))

    idx = 0
    for _, row in data.iterrows():
        for value in row:
            feature = algo.convert(str(value))
            features[idx] = feature
            idx = idx + 1

    predicted = model.predict(features)

    predicted = predicted.reshape(nb_rows, nb_cols)

    # TODO I'm sure it's not a good way to do it...
    result = [
        types.get_type_by_label(pd.value_counts(predicted[:, c]).index[0])
        for c in range(nb_cols)
    ]

    return result


def guess(data):

    # get algo to compute features
    conf = dict(settings.STR2FEATURES_CONF)
    algo_features = getattr(str2features, conf.pop("algo"))(**conf)

    with open(settings.MODEL_PATH, "rb") as f:
        # load model
        model = pickle.load(f)

    # predict column types
    column_type = predict(data, model, algo_features)

    return column_type
