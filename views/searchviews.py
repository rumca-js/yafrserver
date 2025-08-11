from utils.sqlmodel import Gateway, SearchView
from views.views import *
from rsshistory.configuration import Configuration


def v_gateways(request):
    c = Configuration.get_object()
    c.model

    text = """
        <h1>Gateways</h1>
        <ul>
    """

    gateways = c.model.all(Gateway)
    for gateway in gateways:
        gateway_description = ""
        if gateway.description:
            gateway_description = f" - ${gateway.description}"

        text += f"""
        <li>
            <a href="{gateway.link}" title="{gateway.title}">
              <img scr="/static/icons/" />
              {gateway.title} @ {gateway.link}
              {gateway_description}
            </a>
        </li>
        """

    text += "</ul>"

    return get_html(id=0, body=text, title="Gateways")


def v_search_internet(request):
    c = Configuration.get_object()
    c.model

    text = """
        <h1>Search views</h1>
        <ul>
    """

    gateways = c.model.all(Gateway)
    for gateway in gateways:
        gateway_description = ""
        if gateway.description:
            gateway_description = f" - ${gateway.description}"

        text += f"""
        <li>
            <a href="{gateway.link}" title="{gateway.title}">
              <img scr="/static/icons/" />
              {gateway.title} @ {gateway.link}
              {gateway_description}
            </a>
        </li>
        """

    text += "</ul>"

    return get_html(id=0, body=text, title="Searchviews")
