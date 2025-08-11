from flask import request, jsonify
from utils.sqlmodel import SearchView
from rsshistory.status import Status
from rsshistory.configuration import Configuration
from views.views import get_html


def v_index(request):
    id = 0
    c = Configuration.get_object()

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


def v_search(request):
    text = """
    <form action="/entries" method="get">
        <input type="text" name="query" placeholder="Search..." required>
        <button type="submit">Search</button>
    </form>

    <div><a href="/entries?link=youtube.com">YouTube</a></div>
    <div><a href="/entries?link=reddit.com">Reddit</a></div>
    """

    return get_html(id=0, body=text, title="Search")

def v_get_indicators(request):
    c = Configuration.get_object()
    status = Status.get_object()

    indicators = {}

    sources_queue_size = 0
    sources_are_fetched = False
    read_later_queue_size = 0
    read_later_status = False
    is_sources_error = False
    is_internet_error = False
    is_remote_server_down = False
    threads_error = False
    is_backgroundjobs_error = False
    is_configuration_error = False

    indicators["is_reading"] = {}
    indicators["is_reading"]["message"] = f"Sources queue:{sources_queue_size}"
    indicators["is_reading"]["status"] = sources_are_fetched

    indicators["read_later_queue"] = {}
    indicators["read_later_queue"][
        "message"
    ] = f"Read later queue {read_later_queue_size}"
    indicators["read_later_queue"]["status"] = read_later_status

    indicators["sources_error"] = {}
    indicators["sources_error"]["message"] = f"Sources error"
    indicators["sources_error"]["status"] = is_sources_error

    indicators["internet_error"] = {}
    indicators["internet_error"]["message"] = f"Internet error"
    indicators["internet_error"]["status"] = is_internet_error

    indicators["crawling_server_error"] = {}
    indicators["crawling_server_error"]["message"] = f"Crawling server error"
    indicators["crawling_server_error"]["status"] = is_remote_server_down

    indicators["threads_error"] = {}
    indicators["threads_error"]["message"] = f"Threads error"
    indicators["threads_error"]["status"] = threads_error

    indicators["jobs_error"] = {}
    indicators["jobs_error"]["message"] = f"Jobs error"
    indicators["jobs_error"]["status"] = is_backgroundjobs_error

    indicators["configuration_error"] = {}
    indicators["configuration_error"]["message"] = f"Configuration error"
    indicators["configuration_error"]["status"] = is_configuration_error

    data = {"indicators": indicators}
    return jsonify(data)


def v_get_search_container(request):
    c = Configuration.get_object()

    data = {}

    rows = []

    row = {}
    row["link"] = "/search-internet"
    row["icon"] = "/static/icons/icons8-search-100.png"
    row["title"] = "Search Internet"
    rows.append(row)

    row = {}
    row["link"] = "/gateways"
    row["icon"] = "/static/icons/icons8-search-100.png"
    row["title"] = "Gateways"
    rows.append(row)

    for searchview in c.model.all(SearchView):
        row = {}
        row["link"] = "/entries?v=" + searchview.id
        row["icon"] = "/static/icons/icons8-search-100.png"
        row["title"] = searchview.name
        rows.append(row)

    data["rows"] = rows
    data["title"] = "Search"

    return jsonify(data)


def v_get_global_container(request):
    data = {}

    rows = []

    row = {}
    row["link"] = "/sources"
    row["icon"] = "/static/icons/icons8-search-100.png"
    row["title"] = "Sources"
    rows.append(row)

    row = {}
    row["link"] = "/entries"
    row["icon"] = "/static/icons/icons8-search-100.png"
    row["title"] = "Entries"
    rows.append(row)

    data["rows"] = rows
    data["title"] = "Global"

    return jsonify(data)


def v_get_personal_container(request):
    data = {}

    rows = []

    row = {}
    row["link"] = "/user-search-history"
    row["icon"] = "/static/icons/icons8-search-100.png"
    row["title"] = "Search history"
    rows.append(row)

    row = {}
    row["link"] = "/user-browse-history"
    row["icon"] = "/static/icons/icons8-search-100.png"
    row["title"] = "Browse history"
    rows.append(row)

    data["rows"] = rows
    data["title"] = "Personal"

    return jsonify(data)


def v_get_tools_container(request):
    data = {}

    rows = []

    row = {}
    row["link"] = "/page-show-props"
    row["icon"] = "/static/icons/icons8-search-100.png"
    row["title"] = "Page Properties"
    rows.append(row)

    data["rows"] = rows
    data["title"] = "Tools"

    return jsonify(data)


def v_get_users_container(request):
    data = {}

    rows = []

    row = {}
    row["link"] = "/admin"
    row["icon"] = "/static/icons/icons8-search-100.png"
    row["title"] = "Admin"
    rows.append(row)

    data["rows"] = rows
    data["title"] = "Users"

    return jsonify(data)


def v_admin(request):
    text = get_template("admin_page.html")
    return get_html(id=0, body=text, title="Admin")
