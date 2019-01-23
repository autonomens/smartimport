""" Describe all guessable type """

import sys
import inspect
import itertools

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


label_gen = itertools.count(0)


class Unknown(GuessableType):
    """ Default type if type can't be determined """

    name = "unknown"
    label = next(label_gen)


class PhoneNumber(GuessableType):
    name = "phonenumber"
    label = next(label_gen)

    # TODO  use https://github.com/daviddrysdale/python-phonenumbers

    def anomalie_score(self, value):
        # TODO define a phone number regex to allow detecting bad number
        return 0.0

    def clean_value(self, value):
        value = super().clean_value(value)
        return value


class URL(GuessableType):
    name = "url"
    label = next(label_gen)


class Zipcode(GuessableType):
    name = "zipcode"
    label = next(label_gen)


class CityName(GuessableType):
    name = "city"
    label = next(label_gen)


class Date(GuessableType):
    name = "date"
    label = next(label_gen)

    # TODO use https://dateparser.readthedocs.io/en/latest/


class CompagnyName(GuessableType):
    name = "compagny_name"
    label = next(label_gen)


class Number(GuessableType):
    name = "number"
    label = next(label_gen)

    def _clean_value(self, value):
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
    label = next(label_gen)


class Cedex(GuessableType):
    name = "cedex"
    label = next(label_gen)


class DepartementCode(GuessableType):
    name = "department_code"
    label = next(label_gen)


class BrandName(GuessableType):
    name = "brand_name"
    label = next(label_gen)


class NafCode(GuessableType):
    name = "naf_id"
    label = next(label_gen)


class CountryName(GuessableType):
    name = "country"
    label = next(label_gen)


class Year(GuessableType):
    name = "year"
    label = next(label_gen)


class Coordinate(GuessableType):
    name = "coordinate"
    label = next(label_gen)


class PersonLastame(GuessableType):
    name = "person_lastname"
    label = next(label_gen)


class PersonFirstname(GuessableType):
    name = "person_firstname"
    label = next(label_gen)


class MuseumName(GuessableType):
    name = "museum_name"
    label = next(label_gen)


class CountryCode(GuessableType):
    name = "country_code"
    label = next(label_gen)


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
