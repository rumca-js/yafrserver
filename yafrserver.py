"""
This is example script about how to use this project as a simple RSS reader
"""
import json
import time
import threading

from sqlalchemy import (
    create_engine,
)

from flask import Flask, request, jsonify, Response

from utils.sqlmodel import SqlModel
from rsshistory.webtools import (
   WebConfig,
   RemoteServer,
   FeedClient,
   Url,
)


# increment major version digit for releases, or link name changes
# increment minor version digit for JSON data changes
# increment last digit for small changes
__version__ = "4.0.20"


engine = create_engine("sqlite:///feedclient.db")
#model = SqlModel(engine=engine)
client = FeedClient(engine=engine)

entries_per_page = 200

app = Flask(__name__)


def get_html(id, body, title="", index=False):
    if not index:
        if not id:
            id = ""
        body = '<a href="/?id={}">Back</a>'.format(id) + body

    html = """<!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/jszip/dist/jszip.min.js"></script>

        <link rel="stylesheet" href="/static/css/styles.css_style-light.css?1753905798">
        <script src="/static/library.js?=7"></script>
        <script src="/static/entries_library.js?=7"></script>

        <title>{}</title>
    </head>
    <body>
    {}
    </body>
    </html>
    """.format(
        title, body
    )

    return html


@app.route("/")
def index():
    id = 0

    # fmt: off

    command_links = []
    command_links.append({"link" : "/entries", "name":"entries", "description":"Shows entries"})
    command_links.append({"link" : "/sources", "name":"sources", "description":"Shows sources"})
    command_links.append({"link" : "/search", "name":"search", "description":"Search"})

    # fmt: on

    text = """<h1>Commands</h1>"""

    for link_data in command_links:
        text += """<div><a href="{}?id={}">{}</a> - {}</div>""".format(
            link_data["link"], id, link_data["name"], link_data["description"]
        )

    return get_html(id=id, body=text, title="Yafr server", index=True)


@app.route("/entries")
def entries():
    text = ""

    link = request.args.get("link") or ""
    source_id = request.args.get("source")
    page = request.args.get("page") or ""

    index = 0

    entry_id = request.args.get("id")
    link = f"/entries-json?link={link}&page={page}"

    text = """
    <div id="listData"></div>
    <script>
        let view_display_type = "standard";
        let view_show_icons = true;
        let view_small_icons = false;
        let show_pure_links = false;
        let highlight_bookmarks = false;
        let sort_function = "-date_published"; // page_rating_votes, date_published
        let default_page_size = {};

       getDynamicJson("{}", function(entries) {{
          var finished_text = getEntriesList(entries);
          $('#listData').html(finished_text);
       }});
    </script>
    """.format(entries_per_page, link)

    return get_html(id=0, body=text, title="Entries")


def entry_to_json(entry):
    json = {}
    json["id"] = entry.id
    json["title"] = entry.title
    json["description"] = entry.description
    json["link"] = entry.link
    json["date_published"] = str(entry.date_published)
    json["status_code"] = entry.status_code
    json["thumbnail"] = entry.thumbnail
    json["language"] = entry.language
    json["permanent"] = entry.permanent
    json["author"] = entry.author
    json["album"] = entry.album

    return json

def source_to_json(source):
    json = {}
    json["title"] = source.title
    json["url"] = source.url

    return json


@app.route("/entries-json")
def entries_json():
    link = request.args.get("link")
    page = request.args.get("page") or 1
    source_id = request.args.get("source")

    page = int(page)

    index = 0
    entries_json = []

    entries = client.get_entries(page=page, rows_per_page=entries_per_page)
    for entry in reversed(entries):
        if link and entry.link.find(link) == -1:
            continue

        if source_id and entry.source != int(source_id):
            continue

        index += 1
        if index > entries_per_page:
            break

        entry_json = entry_to_json(entry)

        entries_json.append(entry_json)

    return jsonify(entries_json)


@app.route("/entry-json")
def entry_json():
    link = request.args.get("link")
    id = request.args.get("id")

    entry_json = {}

    entry = client.get_entry(id=id)
    if entry:
        entry_json = entry_to_json(entry)

    return jsonify(entry_json)


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
    id = request.args.get("id")

    link = f"/entry-json?id={id}"

    text = """
    <div class="container">
       <div id="entryData"></div>
    </div>
    <script>
        let view_display_type = "standard";
        let view_show_icons = true;
        let view_small_icons = false;
        let show_pure_links = false;
        let highlight_bookmarks = false;
        let sort_function = "-date_published";
        let default_page_size = {};

        getDynamicJson("{}", function(entry) {{
            var finished_text = getEntryDetailText(entry);
            $('#entryData').html(finished_text);

            document.title = entry.title;
        }});
    </script>
    """.format(entries_per_page, link)

    return get_html(id=0, body=text, title="Entries")


@app.route("/sources")
def sources():
    text = ""

    link = request.args.get("link")
    index = 0

    sources = client.get_sources()
    for source in sources:
        if link and source.url.find(link) == -1:
            continue

        index += 1

        if index > entries_per_page:
            break

        text += """
            <a href="/source?id={}" style="display: flex; align-items: center; gap: 10px; text-decoration: none; color: inherit; margin-bottom: 10px;">
                <img src="{}" width="100px" style="flex-shrink: 0;"/>
                <div>
                    <div>{}</div>
                    <div>{}</div>
                </div>
            </a>
            """.format(source.id, source.favicon, source.url, source.title)

    return get_html(id=0, body=text, title="Sources")


@app.route("/source")
def source():
    text = ""

    link = request.args.get("link")
    id = request.args.get("id")
    index = 0

    source = client.get_source(id=id)

    if source:
        text += """
                <img src="{}" width="100px" style="flex-shrink: 0;"/>
                <div>
                    <div>{}</div>
                    <div>{}</div>
                    <div>{}</div>
                    <a href="/entries?source={}">Entries</a>
                </div>
            """.format(source.favicon, source.id, source.title, source.url, source.id)
    else:
        text = "Not found"

    return get_html(id=0, body=text, title="Source")


def fetch(url):
    request_server = RemoteServer("http://127.0.0.1:3000")

    all_properties = request_server.get_getj(url, name="RequestsCrawler")
    return all_properties


def read_sources(file):
    with open(file, "r") as fh:
        contents = fh.read()
        return json.loads(contents)


def background_refresh():
    news_sources = read_sources("init_sources_news.json")
    for source in news_sources:
        url = source["url"]
        #print(url)
        client.follow_url(url)

    while True:
        client.refresh()
        time.sleep(60*10) # every 10 minutes


def start_server():
    host = "0.0.0.0"
    port=8000

    context = None
    app.run(debug=True, host=host, port=port, threaded=True)


def main():
    WebConfig.init()

    # Start refresh in a daemon thread
    refresh_thread = threading.Thread(target=background_refresh, daemon=True)
    refresh_thread.start()

    start_server()


if __name__ == "__main__":
    main()
