"""
This is example script about how to use this project as a simple RSS reader
"""
import json
import time
import threading
import os

from flask import Flask, request, jsonify, Response

from utils.controllers import (
    EntriesTableController,
)
from utils.controllers.sourcesreader import SourceReader
from rsshistory.webtools import (
   WebConfig,
   RemoteServer,
)
from rsshistory.configuration import Configuration
from rsshistory.status import Status
from views.entries import v_entries, v_entries_json, v_entry, v_entry_json
from views.sources import v_sources, v_sources_json, v_source
from views.views import get_html



status = Status()
c = Configuration()

app = Flask(__name__)


@app.route("/")
def index():
    id = 0

    # fmt: off

    command_links = []
    command_links.append({"link" : "/entries", "name":"entries", "description":"Shows entries"})
    command_links.append({"link" : "/sources", "name":"sources", "description":"Shows sources"})

    # fmt: on
    text = ""
    text += "<div class='container'>"

    text += """
    <h1>Commands</h1>
    """

    for link_data in command_links:
        text += """<div><a href="{}?id={}">{}</a> - {}</div>""".format(
            link_data["link"], id, link_data["name"], link_data["description"]
        )

    text += """ <h1>Info</h1> """
    text += f""" <div>Crawler server= {c.crawler_server}:{c.crawler_port}</div>"""
    text += f""" <div>DB= {c.database_file_name}</div>"""

    text += "</div>"

    return get_html(id=id, body=text, title="Yafr server", index=True)


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
    text = """
    <form action="/entries" method="get">
        <input type="text" name="query" placeholder="Search..." required>
        <button type="submit">Search</button>
    </form>

    <div><a href="/entries?link=youtube.com">YouTube</a></div>
    <div><a href="/entries?link=reddit.com">Reddit</a></div>
    """

    return get_html(id=0, body=text, title="Search")


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
    text = ""

    id = request.args.get("entry_id")

    # what if it is in archive

    entry = EntriesTableController(db = c.model).get(id=id)

    if not entry:
        return jsonify(
            {"errors": ["Entry does not exists"]}
        )

    remote_server = RemoteServer(c.crawler_location)

    json_obj = remote_server.get_socialj(entry.link)
    if not json_obj:
        return jsonify(
            {"errors": ["Could not obtain social data"]},
        )

    try:
        return jsonify(json_obj)
    except Exception as E:
        return jsonify(
                {"errors": ["Could not dump social data: {}".format(E)]},
        )

    return get_html(id=0, body=text, title="Source")


def fetch(url):
    request_server = RemoteServer(c.crawler_location)

    all_properties = request_server.get_getj(url)
    return all_properties


def read_sources(file):
    with open(file, "r") as fh:
        contents = fh.read()
        return json.loads(contents)


def background_refresh():
    from utils.controllers.sources import SourceDataBuilder
    status = Status.get_object()

    print("-----Reading sources-----")

    news_sources = read_sources("init_sources_news.json")
    status.reading_sources = True
    for key, source in enumerate(news_sources):
        builder = SourceDataBuilder(conn=c.model)
        source["id"] = key
        try:
            source_obj = builder.build(link_data = source)
            if source_obj:
                print("Built {}".format(source["url"]))
        except Exception as E:
            print(str(E))
    status.reading_sources = False

    remote_server = RemoteServer(c.crawler_location)
    print("-----Starting operation-----")

    reader = SourceReader(db = c.model)
    
    while True:
        print("In a loop")
        if remote_server.is_ok():
            status.reading_entries = True
            reader.read()
            status.reading_entries = False
        else:
            print(f"Server is not OK {c.crawler_location}")

        time.sleep(60*10) # every 10 minutes


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

    # Start refresh in a daemon thread
    refresh_thread = threading.Thread(target=background_refresh, daemon=True)
    refresh_thread.start()

    start_server()


if __name__ == "__main__":
    main()
