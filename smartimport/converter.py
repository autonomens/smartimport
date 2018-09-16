import pandas as pd
import numpy as np

from smartimport import guesser

def dataset_to_json(row, headers):
    res = {}

    # Get guessed type for whole data set
    # TODO not implemented yet
    res["predicted_type"] = [("unknown", 1.0)]

    res["properties"] = []

    for h, value in zip(headers, row):
        guessed_type = h['guessed_type']
        
        if str(value) == 'nan': # Remove nan values
            value = None

        # save column element analyse
        res["properties"].append(
            {
                "original_value": value,
                "value": guessed_type.clean_value(value),
                # 'fixed_value' : guessed_type.fix_value(value, dataset.values),
                # 'anomaly_score' : guessed_type.anomaly_score(value),
                # 'associated_properties' : guessed_type.complete_data(value, dataset.values),
            }
        )

    return res

def convert(input_file):
    """ Convert input table to json data """

    data = pd.read_table(
        input_file,
        sep=None,
        engine="python",
    )

    headers = guesser.guess(data)

    result = []

    for row in data.values:
        result.append(dataset_to_json(row, headers))

    return {'headers': headers, 'content': result}