import os
import json
import pickle
import pandas as pd

from smartimport import settings


def convert(file_path):
    """
    Analyse a file and guess column types.

    :param file_path: path of the file containg original data
    :return: result of the analysis in a json serializable object
    """


