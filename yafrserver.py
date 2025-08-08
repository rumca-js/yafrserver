"""
This is example script about how to use this project as a simple RSS reader
"""
import os

from flask import Flask, request, jsonify, Response

from utils.controllers import (
    EntriesTableController,
)
from rsshistory.webtools import (
   WebConfig,
   RemoteServer,
)
from rsshistory.configuration import Configuration
from rsshistory.status import Status
from views.entries import v_entries, v_entries_json, v_entry, v_entry_json, v_entry_dislikes
from views.sources import v_sources, v_sources_json, v_source
from views.system import v_index, v_search
from views.views import get_html



status = Status()
c = Configuration()

app = Flask(__name__)


@app.route("/")
def index():
    return v_index(request)


@app.route("/entries")
def entries():
    return v_entries(request)


@app.route("/entries-json")
def entries_json():
    return v_entries_json(request)


@app.route("/entry-json")
def entry_json():
    return v_entry_json(request)


@app.route("/search")
def search():
    return v_search(request)


@app.route("/entry")
def entry():
    return v_entry(request)


@app.route("/sources")
def sources():
    return v_sources(request)


@app.route("/sources-json")
def sources_json():
    return v_sources_json(request)


@app.route("/source")
def source():
    return v_source(request)


@app.route("/entry-dislikes")
def entry_dislikes():
    return v_entry_dislikes(request)


def start_server():
    host = "0.0.0.0"
    port=8777

    if "YAFR_HOST" in os.environ:
        host = os.environ["YAFR_HOST"]
    if "YAFR_PORT" in os.environ:
        port = int(os.environ["YAFR_PORT"])

    context = None
    app.run(debug=True, host=host, port=port, threaded=True)


def main():
    WebConfig.init()
    config = c.config_entry
    print(config.instance_title)

    start_server()


if __name__ == "__main__":
    main()
