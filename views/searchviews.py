from flask import request, jsonify

from utils.sqlmodel import Gateway, SearchView
from views.views import *
from rsshistory.configuration import Configuration


def v_gateways(request):
    c = Configuration.get_object()

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


def v_searchviews_initialize(request):
    c = Configuration.get_object()

    c.model.truncate(SearchView)

    priority = 0

    Session = c.model.get_session()
    with Session() as session:
        view = SearchView(
            name="Default",
            order_by="-page_rating_votes, -page_rating, link",
            default=True,
            hover_text="Search",
            priority=priority,
        )
        session.add(view)

        priority += 1
        view = SearchView(
            name="Bookmarked",
            filter_statement="bookmarked=True",
            order_by="-date_created, link",
            user=True,
            hover_text="Search bookmars",
            priority=priority,
        )
        session.add(view)

        priority += 1
        view = SearchView(
            name="Search by votes",
            order_by="-page_rating_votes, -page_rating, link",
            entry_limit=1000,
            hover_text="Searches by rating votes",
            priority=priority,
        )
        session.add(view)

        priority += 1
        view = SearchView(
            name="What's created",
            order_by="-date_created, link",
            date_published_day_limit=7,
            hover_text="Search by date created",
            priority=priority,
        )
        session.add(view)

        priority += 1
        view = SearchView(
            name="What's published",
            order_by="-date_published, link",
            date_published_day_limit=7,
            hover_text="Search by date published",
            priority=priority,
        )
        session.add(view)

        priority += 1
        view = SearchView(
            name="Search all",
            order_by="-date_created, link",
            hover_text="Searches all entries",
            priority=priority,
        )
        session.add(view)
        session.commit()

    data = {}
    data["message"] = "OK"
    data["status"] = True
    return jsonify(data)
