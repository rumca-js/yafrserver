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
