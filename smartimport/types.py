""" Describe all guessable type """

import sys
import inspect

# TODO add common names for each types to add guessing probability
# TODO add thematic to allow file type determination
# TODO add some conversion function to avoid bad cleaning


class GuessableType:
    name = ":Unamed:"
    label = -1

    def anomaly_score(self, value):
        return 0.0

    def clean_value(self, value):
        """ Clean the value """
        if value is None:
            return ""
        return value

    def fix_value(self, value, dataset):
        """ Fix value if needed """
        return [(value, 1.0)]

    def complete_data(self, value, dataset):
        """ Add side data """
        return []

    def populate_header(self, header_dict, data):
        """ Add data to header if necessary """
        return header_dict

    @property
    def header_name(self):
        return f"{self.name}"

    def to_json(self):
        return f"{self.name}"

    def __str__(self):
        return f"<{self.name}({self.label})>"

    def __repr__(self):
        return f"<{self.name.upper()}({self.label})>"


class Unknown(GuessableType):
    """ Default type if type can't be determined """

    name = "unknown"
    label = 0


class PhoneNumber(GuessableType):
    name = "phone_number"
    label = 1

    # TODO  use https://github.com/daviddrysdale/python-phonenumbers

    def anomalie_score(self, value):
        # TODO define a phone number regex to allow detecting bad number
        return 0.0

    def clean_value(self, value):
        value = super().clean_value(value)
        return value


class URL(GuessableType):
    name = "url"
    label = 2


class Zipcode(GuessableType):
    name = "zipcode"
    label = 3


class CityName(GuessableType):
    name = "city"
    label = 4


class Date(GuessableType):
    name = "date"
    label = 5

    # TODO use https://dateparser.readthedocs.io/en/latest/


class CompagnyName(GuessableType):
    name = "compagny_name"
    label = 6


class Number(GuessableType):
    name = "number"
    label = 7

    def clean_value(self, value):
        """ Clean the value """
        if value is None:
            return ""
        try:
            return str(int(value))
        except ValueError:
            print(f"Can't convert {value}")
            return str(value)


class Address(GuessableType):
    name = "address"
    label = 8


class AddressSecondLine(GuessableType):
    name = "address_secondline"
    label = 9


class AddressThirdLine(GuessableType):
    name = "address_thirdline"
    label = 10


class AddressStreetLine(GuessableType):
    name = "address_streetline"
    label = 10


class AddressStreetLineNumber(GuessableType):
    name = "address_streetline_number"
    label = 11


class AddressStreetLineCount(GuessableType):
    name = "address_streetline_count"
    label = 12


class AddressStreetLineType(GuessableType):
    name = "address_streetline_type"
    label = 13


class AddressStreetLineName(GuessableType):
    name = "address_streetline_name"
    label = 14


class Cedex(GuessableType):
    name = "cedex"
    label = 15


class DepartementCode(GuessableType):
    name = "department_code"
    label = 16


class BrandName(GuessableType):
    name = "brand_name"
    label = 17


class NafCode(GuessableType):
    name = "naf_id"
    label = 18


class CountryName(GuessableType):
    name = "country"
    label = 19


class Year(GuessableType):
    name = "year"
    label = 20


class Coordinate(GuessableType):
    name = "coordinate"
    label = 21


class PersonName(GuessableType):
    name = "person_name"
    label = 22
    

class PersonSurname(GuessableType):
    name = "person_surname"
    label = 23


class MuseumName(GuessableType):
    name = "museum_name"
    label = 24


# TODO Add region, department, museum, insee, school, 
# association, money, firstname_m, firstname_w, lastname, gender

# map to convert two ways
_all_by_type = {}
_all_by_label = {}


def get_all_guessable_types():
    global _all_by_type
    global _all_by_label

    if not _all_by_type:
        result = []
        for _, obj in inspect.getmembers(sys.modules[__name__]):
            if (
                inspect.isclass(obj)
                and issubclass(obj, GuessableType)
                and obj is not GuessableType
            ):
                result.append(obj)
        _all_by_type = {C.name: C() for C in result}
        _all_by_label = {c.label: c for k, c in _all_by_type.items()}

    return _all_by_type


def get_type_by_label(label):
    if not _all_by_label:
        get_all_guessable_types()

    return _all_by_label[label]


def label_to_type(label):
    if not _all_by_label:
        get_all_guessable_types()

    return _all_by_label[label].name


def type_to_label(type_name):
    return get_all_guessable_types()[type_name].label
