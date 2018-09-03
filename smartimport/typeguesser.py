""" Describe all guessable type """


class GuessableType:

    def __init__(self, name):
        self.name = name

    def anomaly_score(self, value):
        return 0.0

    def clean_value(self, value):
        return value.strip()

    def fix_value(self, value, dataset):
        return [(value, 1.0)]

    def complete_data(self, value, dataset):
        return []

    def to_json(self, value):
        return {}

class Unknown(GuessableType):
    """ Default type if type cant be determined """

    def __init__(self):
        super().__init__('unknown')

class PhoneNumber(GuessableType):

    def __init__(self):
        super().__init__('phone_number')

    def anomalie_score(self, value):
        # TODO define a phone number regex to allow detecting bad number
        return 0.0

    def fix_value(self, value, dataset):
        # TODO Add phone number formatter
        return [(value, 1.0)]

class URL(GuessableType):
    
    def __init__(self):
        super().__init__('url')


class Zipcode(GuessableType):
    
    def __init__(self):
        super().__init__('zipcode')

class CityName(GuessableType):
    
    def __init__(self):
        super().__init__('city_name')

class Date(GuessableType):
    
    def __init__(self):
        super().__init__('date')

class CompagnyName(GuessableType):
    
    def __init__(self):
        super().__init__('compagny_name')

# TODO add other guessable types

def guess(data):
    # TODO implement this algo
    # Extract file first xxx lines
    # Apply model to guess models
    # Return list of all Guessable types for each column

    import random
    result = [random.choices([PhoneNumber, CityName, Date]) for _ in range(data.size[1])]

    return result