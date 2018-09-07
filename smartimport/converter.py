import os
import json
import pickle
import pandas as pd

from smartimport import settings
from smartimport import typeguesser

def read_file_by_chunk(input_file, chunk_size=200):
    """
    Generator to read file chunk by chunk.

    :param input_file: File object to read
    :return: part of the file as Pandas dataframe.
    """

    for df in pd.read_table(input_file,  dtype='str', sep=None, engine='python', chunksize=chunk_size):
        yield df

def dataset_to_json(dataset, guessed_types):
    res = {}

    # Get guessed type for whole data set
    res['predicted_type'] = [('unknown', 1.0)]

    res['properties'] = []

    original_names = dataset.index.values
    # for each column
    for idx, value in enumerate(dataset.values):
        # to get orignal names of the columns
        guessed_type = guessed_types[idx]

        # save column element analyse
        res['properties'].append({
            'type' : guessed_type.name,
            'original_name' : original_names[idx],
            'original_value' : value,
            'value' : guessed_type.clean_value(value),
            'fixed_value' : guessed_type.fix_value(value, dataset.values),
            'anomaly_score' : guessed_type.anomaly_score(value),
            'associated_properties' : guessed_type.complete_data(value, dataset.values),
        })

    return res


def convert(input_file):
    """
    Analyse a file and guess column types.

    :param file_path: file object containg original data
    :return: result of the analysis in a json serializable object
    """

    header = next(read_file_by_chunk(input_file, chunk_size=250 ))

    guessed_types = typeguesser.guess(header)

    for chunk in read_file_by_chunk(input_file):
        result = chunk.apply(lambda row: dataset_to_json(row, guessed_types), axis=1)

        yield result.values.tolist()








