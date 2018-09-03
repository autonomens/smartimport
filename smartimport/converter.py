import os
import json
import pickle
import pandas as pd

from smartimport import settings
from smartimport import typeguesser

def read_file_by_chunk(file_path, chunk_size=200):
    """
    Generator to read file chunk by chunk.

    :param file_path: File to read
    :return: part of the file as Pandas dataframe.
    """
    # Compute file extension.
    filename, file_ext = os.path.splitext(file_path)

    # For now, use the extension as filetype.
    # TODO: eventually use python-magic
    if (file_ext == '.csv'):
        reader = pd.read_csv
    elif (file_ext == '.xls'):
        reader = pd.read_excel
    elif (file_ext == '.json'):
        reader = pd.read_json
    elif (file_ext == '.xml'):
        # Pandas does not read XML natively.
        # TODO… (http://www.austintaylor.io/lxml/python/pandas/xml/dataframe/2016/07/08/convert-xml-to-pandas-dataframe/)
        raise RuntimeError('Unable to read xml files')
    else:
        raise RuntimeError('Unsupported file type')

    for df in reader(file_path,  dtype='str', sep=None, engine='python', chunksize=chunk_size):
        yield df 


def dataset_to_json(dataset, guessed_types):
    res = {}

    # Get guessed type for whole data set
    res['predicted_type'] = []

    res['properties'] = []

    # for each column
    for idx, value in enumerate(dataset.values):
        # to get orignal names of the columns
        original_names = dataset.index.values
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


def convert(file_path):
    """
    Analyse a file and guess column types.

    :param file_path: path of the file containg original data
    :return: result of the analysis in a json serializable object
    """

    header = next(read_file_by_chunk(file_path, chunk_size=250 ))

    guessed_types = typeguesser.guess(header)

    for chunk in read_file_by_chunk(file_path):
        chunk.apply(lambda row: dataset_to_json(row, guessed_types))

        yield chunk.values.tolist()








