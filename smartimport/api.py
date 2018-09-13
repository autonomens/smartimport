import os
import tempfile, shutil

import bottle
from bottle import abort, post, get, request, run, route, view, static_file

from smartimport import converter, settings

ALLOWED_EXT = (".csv",)


@route("/static/<filename:path>")
def server_static(filename):
    """ static files which are in static directory """
    return static_file(filename, root=os.path.join(settings.SRC_DIR, "static"))


@get("/smartimport")
@view("smartimport.tpl")
def get_data_file():
    """ Default template when sending a file """
    return {}


@post("/smartimport")
def convert_file():
    # get data file
    data_file = request.files.get("data_file")

    # check a file is giveninput_data
    if data_file is None:
        return abort(400, "Missing file")

    # check extension
    _, ext = os.path.splitext(data_file.filename)
    if ext not in ALLOWED_EXT:
        return abort(400, "Extension not allowed")

    result = []

    # create temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=True) as temp_file:
        data_file.save(temp_file.name, overwrite=True)

        # And read it
        with open(temp_file.name) as input_file:
            # analyze file using smart import
            for chunk in converter.convert(input_file):
                for row in chunk:
                    result.append(row)

    return {"file": data_file.filename, "result": result}


def run_server(debug=False, host="localhost", port="8080"):
    bottle.TEMPLATE_PATH = [os.path.join(settings.SRC_DIR, "views")]
    if debug:
        run(host=host, port=port, debug=True, reloader=True)
    else:
        run(server="gunicorn", host=host, port=port)
