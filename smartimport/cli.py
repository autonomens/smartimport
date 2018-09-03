"""Console script for smartimport."""
import sys
import begin
import smartimport

# TODO: remove below if statement asap. This is a workaround for a bug in begins
# TODO: which provokes an exception when calling pypeman without parameters.
# TODO: more info at https://github.com/aliles/begins/issues/48
if len(sys.argv) == 1:
    sys.argv.append('-h')

@begin.subcommand
def load(file_path=""):
    """ Load a file and convert to a json stream. """
    pass

@begin.start
def main(version=False):
    """ Smart import file analysis. """
    if version:
        print(smartimport.__version__)
        sys.exit(0)



