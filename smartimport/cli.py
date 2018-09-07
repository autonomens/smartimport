"""Console script for smartimport."""
import sys
import json
import begin
import smartimport
from smartimport import converter, api

# TODO: remove below if statement asap. This is a workaround for a bug in begins
# TODO: which provokes an exception when calling pypeman without parameters.
# TODO: more info at https://github.com/aliles/begins/issues/48
if len(sys.argv) == 1:
    sys.argv.append('-h')

@begin.subcommand
def train():
    """ Train a model from dataset (not working yet)"""

@begin.subcommand
def load(file_path:'path to the file containing data'):
    """ Transform a file from csv to json """

    with open(file_path, 'r') as input_file: 
        # analyze file
        result = []
        for chunk in converter.convert(input_file):
            for row in chunk:
                # TODO stream json later
                result.append(row)

    print(json.dumps(result))

@begin.subcommand
def serve(debug=False):
    api.run_server(debug=debug, host='localhost', port=8080)

@begin.start
def main(version=False):
    """ Smart import file analysis. """
    if version:
        print(smartimport.__version__)
        sys.exit(0)



