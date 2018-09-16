import os
import tempfile

import bottle
from bottle import (
    abort,
    post,
    get,
    request,
    run,
    route,
    view,
    static_file,
    default_app,
    template,
)

from smartimport import converter, settings

ALLOWED_EXT = (".csv",)

bottle.TEMPLATE_PATH = [os.path.join(settings.SRC_DIR, "views")]


@route("/static/<filename:path>")
def server_static(filename):
    """ static files which are in static directory """
    return static_file(filename, root=os.path.join(settings.SRC_DIR, "static"))


@get("/")
@view("form.tpl")
def get_data_file():
    """ Default template when sending a file """
    json_output = request.query.get("json", "False").lower() in ["true", "on", "1"]
    return {"json": json_output}


@post("/")
def convert_file():
    # get data file
    data_file = request.files.get("data_file")
    json_output = request.query.get("json", "False").lower() in ["true", "on", "1"]

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
            result = converter.convert(input_file)

    if json_output:
        return {"file": data_file.filename}.update(result)
    else:

        return template("result.tpl", **result)


def run_debug_server(host, port):
    run(host=host, port=port, debug=True, reloader=True)


app = default_app()
