"""
This is example script about how to use this project as a simple RSS reader
"""
import json
import time
import threading
import os

from sqlalchemy import (
    create_engine,
    or_,
)

from flask import Flask, request, jsonify, Response

from utils.sqlmodel import (
    SqlModel,
    EntriesTable,
    EntriesTableController,
    SourcesTable,
    ConfigurationEntryController,
)
from utils.alchemysearch import AlchemySearch
from utils.controllers.entries import entry_to_json
from rsshistory.webtools import (
   WebConfig,
   RemoteServer,
   Url,
)
from rsshistory.webtools.feedclient import FeedClient


# increment major version digit for releases, or link name changes
# increment minor version digit for JSON data changes
# increment last digit for small changes
__version__ = "4.1.8"


file_name = "feedclient.db"
reading_entries = False
reading_sources = False
entries_per_page = 200

crawler_server = "127.0.0.1"
if "CRAWLER_BUDDY_SERVER" in os.environ:
    crawler_server = os.environ["CRAWLER_BUDDY_SERVER"]
crawler_port = "3000"
if "CRAWLER_BUDDY_PORT" in os.environ:
    crawler_port = os.environ["CRAWLER_BUDDY_PORT"]
crawler_location = f"http://{crawler_server}:{crawler_port}"

engine = create_engine("sqlite:///{}".format(file_name))
#model = SqlModel(engine=engine)

client = FeedClient(engine=engine, server_location=crawler_location)

app = Flask(__name__)


def get_navbar():
    text = """
    <nav id="navbar" class="navbar sticky-top navbar-expand-lg navbar-light bg-light">
      <div class="d-flex w-100">
        <!-- Form with search input -->
        <form action="/entries" method="get" class="d-flex w-100 ms-3" id="searchContainer" style="width: 60%;">
          <div class="input-group">
            <input id="searchInput" name="searchInput" class="form-control me-1 flex-grow-1" type="search" placeholder="Search" autofocus="" aria-label="Search">
            <button id="dropdownButton" class="btn btn-outline-secondary" type="button">⌄</button>
            <button id="searchButton" class="btn btn-outline-success" type="submit">🔍</button>
          </div>
        </form>

        <!-- Navbar toggler button, aligned to the right -->
        <button class="navbar-toggler ms-auto" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>
    
      <div class="collapse navbar-collapse ms-3" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a id="homeButton" class="nav-link" href="/">🏠</a>
          </li>

          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarViewDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              View
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarViewDropdown">
                <li><a id="viewStandard" class="dropdown-item" href="#">Standard</a></li>
                <li><a id="viewGallery" class="dropdown-item" href="#">Gallery</a></li>
                <li><a id="viewSearchEngine" class="dropdown-item" href="#">Search engine</a></li>

                <li><hr class="dropdown-divider"></li>

                <li><a id="displayLight" class="dropdown-item" href="#">Light</a></li>
                <li><a id="displayDark" class="dropdown-item" href="#">Dark</a></li>

                <li><hr class="dropdown-divider"></li>

                <li><a id="orderByVotes" class="dropdown-item" href="#">Order by Votes</a></li>
                <li><a id="orderByDatePublished" class="dropdown-item" href="#">Order by Date published</a></li>
            </ul>
          </li>

          <li class="nav-item">
            <a id="helpButton" class="nav-link" href="#">?</a>
          </li>
        </ul>
      </div>
    </nav>
    """

    return text


def get_html(id, body, title="", index=False):
    if not index:
        if not id:
            id = ""

    reading_entries_text = ""
    reading_sources_text = ""
    if reading_entries:
        reading_entries_text = f""" <div>Reading entries</div>"""
    if reading_sources:
        reading_sources_text = f""" <div>Reading sources</div>"""

    navbar_text = get_navbar()

    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/jszip/dist/jszip.min.js"></script>

        <link rel="stylesheet" href="/static/css/styles.css_style-light.css?1753905798">
        <script src="/static/library.js?=11"></script>
        <script src="/static/entries_library.js?=11"></script>
        <script src="/static/listview.js?=11"></script>

        <title>{title}</title>
    </head>
    <body>

    {navbar_text}

    <div id="searchSuggestions"></div>

    {body}

    <footer id="footer" class="text-center text-lg-start bg-body-tertiary text-muted fixed-bottom">
      <div id="footerStatus" class="text-center p-1" style="display: block;">
        Version:{__version__}
        {reading_entries_text}
        {reading_sources_text}
      </div>
      <div id="footerLine" class="text-center p-1" style="display: none;background-color: rgba(0, 0, 0, 0);">
      </div>
    </footer>

    </body>
    </html>
    """

    return html


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
    text += f""" <div>Crawler server= {crawler_server}:{crawler_port}</div>"""
    text += f""" <div>DB= {file_name}</div>"""

    text += "</div>"

    return get_html(id=id, body=text, title="Yafr server", index=True)


@app.route("/entries")
def entries():
    text = ""

    link = request.args.get("link") or ""
    source_id = request.args.get("source_id")
    page = request.args.get("page") or ""
    search = request.args.get("search") or ""

    index = 0

    entry_id = request.args.get("id")
    link = f"/entries-json?link={link}&page={page}&source_id={source_id}&search={search}"

    text = """
    <div id="listData"></div>
    <script>
        let view_display_type = "standard";
        let view_show_icons = true;
        let view_small_icons = false;
        let show_pure_links = false;
        let highlight_bookmarks = false;
        let sort_function = "-date_published"; // page_rating_votes, date_published

       let loading_text = getSpinnerText();
       $('#listData').html(loading_text);

       getDynamicJson("{}", function(entries) {{
          var finished_text = getEntriesList(entries);
          $('#listData').html(finished_text);
       }});
    </script>
    """.format(link)

    return get_html(id=0, body=text, title="Entries")


#def entry_to_json(entry):
#    json = {}
#    json["id"] = entry.id
#    json["title"] = entry.title
#    json["description"] = entry.description
#    json["link"] = entry.link
#    json["date_published"] = str(entry.date_published)
#    json["status_code"] = entry.status_code
#    json["thumbnail"] = entry.thumbnail
#    json["language"] = entry.language
#    json["permanent"] = entry.permanent
#    json["author"] = entry.author
#    json["album"] = entry.album
#
#    return json

def source_to_json(source):
    json = {}
    json["title"] = source.title
    json["url"] = source.url

    return json


@app.route("/entries-json")
def entries_json():
    link = request.args.get("link") or None
    search = request.args.get("search") or None
    source_id = request.args.get("source_id")
    if source_id == "None":
        source_id = None
    if source_id:
        source_id = int(source_id)
    page = request.args.get("page") or 1
    page = int(page)

    entries_json = []

    search_engine = AlchemySearch(db=engine, page=page, rows_per_page=entries_per_page, search_term=search, ascending=False)
    entries = search_engine.get_filtered_objects()

    for entry in reversed(entries):
        entry_json = entry_to_json(entry)

        entries_json.append(entry_json)

    return jsonify(entries_json)


@app.route("/entry-json")
def entry_json():
    link = request.args.get("link")
    id = request.args.get("entry_id")

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
    id = request.args.get("entry_id")

    link = f"/entry-json?entry_id={id}"

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

        let loading_text = getSpinnerText();
        $('#entryData').html(loading_text);

        getDynamicJson("{}", function(entry) {{
            var finished_text = getEntryDetailText(entry);
            $('#entryData').html(finished_text);

            document.title = entry.title;
        }});
        getDislikeData(1, entry_id={});
    </script>
    """.format(link, id)

    return get_html(id=0, body=text, title="Entries")


@app.route("/sources")
def sources():
    text = ""

    link = request.args.get("link")
    page = request.args.get("page") or 1
    page=int(page)

    sources = client.get_sources(page=page, rows_per_page=entries_per_page)
    for source in sources:
        link = f"/source?page={page}&source_id={source.id}"

        text += """
        <div class="container">
            <a href="{}" style="display: flex; align-items: center; gap: 10px; text-decoration: none; color: inherit; margin-bottom: 10px;">
                <img src="{}" width="100px" style="flex-shrink: 0;"/>
                <div>
                    <div>{}</div>
                    <div>{}</div>
                </div>
            </a>
        </div>
            """.format(link, source.favicon, source.url, source.title)

    return get_html(id=0, body=text, title="Sources")


@app.route("/source")
def source():
    text = ""

    link = request.args.get("link")
    id = request.args.get("source_id")

    source = client.get_source(id=id)

    if source:
        text += """
        <div class="container">
                <img src="{}" width="100px" style="flex-shrink: 0;"/>
                <div>
                    <div>ID: {}</div>
                    <div>{}</div>
                    <div>{}</div>
                    <a href="/entries?source_id={}">Entries</a>
                </div>
        </div>
            """.format(source.favicon, source.id, source.title, source.url, source.id)
    else:
        text = "Not found"

    return get_html(id=0, body=text, title="Source")


@app.route("/entry-dislikes")
def entry_dislikes():
    text = ""

    id = request.args.get("entry_id")

    # what if it is in archive

    entry = client.get_entry(id=id)

    if not entry:
        return jsonify(
            {"errors": ["Entry does not exists"]}
        )

    remote_server = RemoteServer(crawler_location)

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
    request_server = RemoteServer(crawler_location)

    all_properties = request_server.get_getj(url, name="RequestsCrawler")
    return all_properties


def read_sources(file):
    with open(file, "r") as fh:
        contents = fh.read()
        return json.loads(contents)


def background_refresh():
    from utils.controllers.sources import SourceDataBuilder
    global reading_sources, reading_entries, client

    print("-----Reading sources-----")

    news_sources = read_sources("init_sources_news.json")
    reading_sources = True
    for key, source in enumerate(news_sources):
        builder = SourceDataBuilder(conn=client.db)
        source["id"] = key
        print("Building {}".format(source["url"]))
        try:
            builder.build(link_data = source)
        except Exception as E:
            print(str(E))
    reading_sources = False

    remote_server = RemoteServer(crawler_location)
    print("-----Starting operation-----")
    
    while True:
        if remote_server.is_ok():
            reading_entries = True
            client.refresh()
            reading_entries = False

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
    config = ConfigurationEntryController(db=client.db).get()
    print(config.instance_title)

    # Start refresh in a daemon thread
    refresh_thread = threading.Thread(target=background_refresh, daemon=True)
    refresh_thread.start()

    start_server()


if __name__ == "__main__":
    main()
