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
from views.entries import *
from views.sources import *
from views.system import *
from views.searchviews import *
from views.tools import *
from views.userhistory import *
from views.views import *



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


@app.route("/entry-dislikes")
def entry_dislikes():
    return v_entry_dislikes(request)


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


@app.route("/get-indicators")
def get_indicators():
    return v_get_indicators(request)


@app.route("/get-search-container")
def get_search_container():
    return v_get_search_container(request)


@app.route("/get-global-container")
def get_global_container():
    return v_get_global_container(request)


@app.route("/get-personal-container")
def get_personal_container():
    return v_get_personal_container(request)


@app.route("/get-tools-container")
def get_tools_container():
    return v_get_tools_container(request)


@app.route("/get-users-container")
def get_users_container():
    return v_get_users_container(request)


@app.route("/admin")
def admin():
    return v_admin(request)


@app.route("/page-show-props")
def page_show_props():
    return v_page_show_props(request)


@app.route("/user-search-history")
def user_search_history():
    return v_user_search_history(request)


@app.route("/user-browse-history")
def user_browse_history():
    return v_user_browse_history(request)


@app.route("/gateways")
def gateways():
    return v_gateways(request)


@app.route("/search-internet")
def search_internet():
    return v_search_internet(request)


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
