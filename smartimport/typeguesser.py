""" Describe all guessable type """

import inspect, sys


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
    # TODO implement this algo
    # Extract file first xxx lines
    # Apply model to guess models
    # Return list of all Guessable types for each column

    import random
    result = [random.choice(list(get_all_guessable_types().values())) for _ in range(data.shape[1])]

    return result