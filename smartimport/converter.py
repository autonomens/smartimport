import os
import json
import pickle
import pandas as pd

from smartimport import settings
from smartimport import guesser


def read_file_by_chunk(input_file, chunk_size=200):
    """
    Generator to read file chunk by chunk.

    :param input_file: File object to read
    :return: part of the file as Pandas dataframe.
    """

    for df in pd.read_table(
        input_file, dtype="str", sep=None, engine="python", chunksize=chunk_size
    ):
        yield df


def dataset_to_json(dataset, guessed_types):
    res = {}

    # Get guessed type for whole data set
    res["predicted_type"] = [("unknown", 1.0)]

    res["properties"] = []

    original_names = dataset.index.values
    # for each column
    for idx, value in enumerate(dataset.values):
        # to get orignal names of the columns
        guessed_type = guessed_types[idx]

        # save column element analyse
        res["properties"].append(
            {
                "type": guessed_type.name,
                "original_name": original_names[idx],
                "original_value": value,
                "value": guessed_type.clean_value(value),
                # 'fixed_value' : guessed_type.fix_value(value, dataset.values),
                # 'anomaly_score' : guessed_type.anomaly_score(value),
                # 'associated_properties' : guessed_type.complete_data(value, dataset.values),
            }
        )

    return res


def convert(input_file, chunk_size=250, guess_sample_size=200):
    """
    Analyse a file and guess column types.

    :param input_file: file object containg original data
    :return: result of the analysis in a json serializable object
    """

    sample = next(read_file_by_chunk(input_file, chunk_size=guess_sample_size))

    input_file.seek(0)  # Header consume file so we get back

    guessed_types = guesser.guess(sample)

    for chunk in read_file_by_chunk(input_file, chunk_size=chunk_size):
        result = chunk.apply(lambda row: dataset_to_json(row, guessed_types), axis=1)

        yield result.values.tolist()
