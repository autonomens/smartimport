"""Console script for smartimport."""
import sys
import json
import begin
from json import JSONEncoder

import smartimport
from smartimport import converter, trainer

# TODO: remove below if statement asap. This is a workaround for a bug in begins
# TODO: which provokes an exception when calling pypeman without parameters.
# TODO: more info at https://github.com/aliles/begins/issues/48
if len(sys.argv) == 1:
    sys.argv.append("-h")


# Monkey patch to allow json to parse type classes
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default
JSONEncoder.default = _default

@begin.subcommand
def train(confusion: "Show confusion matrix at the end of the process"=False):
    """ Train a model from given dataset"""
    trainer.train(display_confusion_matrix=confusion)


@begin.subcommand
def load(file_path: "path to the file containing data"):
    """ Transform a file from csv to json """

    with open(file_path, "r") as input_file:
        result = converter.convert(input_file)

    #import pdb; pdb.set_trace()

    print(json.dumps(result))


@begin.subcommand
def serve(
    host: "Server host"="localhost", 
    port: "Server port"=8080
):
    """ Start smartimport debug server"""
    from smartimport import api
    api.run_debug_server(host=host, port=port)


@begin.start
def main(version: "Show version and exit"=False):
    """ Smart import file analysis. """
    if version:
        print(smartimport.__version__)
        sys.exit(0)
