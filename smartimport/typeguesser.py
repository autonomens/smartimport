""" Describe all guessable type """

import sys
import json
import inspect
import pickle

import numpy as np

from smartimport import settings, str2features

class GuessableType:

    def anomaly_score(self, value):
        return 0.0

    def clean_value(self, value):
        return value.strip()

    def fix_value(self, value, dataset):
        return [(value, 1.0)]

    def complete_data(self, value, dataset):
        return []


class Unknown(GuessableType):
    """ Default type if type can't be determined """
    name = 'unknown'


class PhoneNumber(GuessableType):
    name = 'phone_number'

    def anomalie_score(self, value):
        # TODO define a phone number regex to allow detecting bad number
        return 0.0

    def fix_value(self, value, dataset):
        # TODO Add phone number formatter
        return [(value, 1.0)]


class URL(GuessableType):
    name = 'url'


class Zipcode(GuessableType):
    name = 'zipcode'


class CityName(GuessableType):
    name = 'city_name'


class Date(GuessableType):
    name = 'date'


class CompagnyName(GuessableType):
    name = 'compagny_name'
    

# TODO add other guessable types

def get_all_guessable_types():
    result = []
    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, GuessableType) and obj is not GuessableType:
            result.append(obj)
    return {C.name: C() for C in result}

def guess(data):

    # get algo to compute features
    conf = dict(settings.STR2FEATURES_CONF)
    algo_features = getattr(str2features, conf.pop('algo'))(**conf)

    with open(settings.MODEL_PATH, 'rb') as f:
        # load model
        model = pickle.load(f)

    # predict column types
    column_types_id = predict(data, model, algo_features)

    with open(settings.ID_TO_TYPE_MAP_PATH) as f:
        # get type name and related idx
        id_to_type_map = json.load(f)

    all_types = get_all_guessable_types()

    result = []
    for type_id in column_types_id:
        result.append(all_types.get(id_to_type_map[str(type_id)], Unknown()))

    return result


def predict(data, model, descriptor_algo):
    """
    :param stream: stream to analyze
    :param model: machine learning trained model to analyse data
    :param descriptor_algo: algorithm to convert original data to features
    :return: a prediction for each column of each row
    """

    # convert stream in features
    nb_rows  = data.shape[0]
    nb_cols = data.shape[1]
    X = np.empty((nb_cols*nb_rows, descriptor_algo.nb_features()))

    idx = 0
    for _, row in data.iterrows():
        for value in row:
            feature = descriptor_algo.convert(str(value))
            X[idx, :] = feature
            idx = idx + 1

    # for each element predict probabilities to belong to each classes
    probas = model.predict_proba(X)

    # to store prediction for each columns
    Y = np.zeros(nb_cols)

    # reshape probas to have values by columns
    nb_classes = probas.size // (nb_cols * nb_rows)
    probas = probas.reshape(nb_rows, nb_cols, nb_classes)

    sum_probas = probas.mean(axis=0)
    Y = sum_probas.argmax(axis=1)

    return Y