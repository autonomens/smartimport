"""Console script for smartimport."""
import sys
import json
import begin
import smartimport

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

    # analyze file
    print('[')
    for chunk in smartimport.converter.convert(file_path):
        # TODO missing json decoration here
        for d in chunk:
            print(json.dumps(d), ',')
    print(']')

@begin.start
def main(version=False):
    """ Smart import file analysis. """
    if version:
        print(smartimport.__version__)
        sys.exit(0)



