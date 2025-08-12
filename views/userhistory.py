from flask import request, jsonify
from sqlalchemy import asc, desc

from views.views import get_html, get_template
from utils.controllers.entries import entry_to_json
from rsshistory.configuration import Configuration
from utils.sqlmodel import UserEntryVisitHistory, UserSearchHistory, EntriesTable


def search_history_to_json(history):
    json_obj = {}
    json_obj["search_query"] = history.search_query
    json_obj["date"] = history.date
    json_obj["user_id"] = history.user_id
    return json_obj


def browse_to_json(history):
    json_obj = {}

    c = Configuration.get_object()
    entry = c.model.get(EntriesTable, history.entry_id)
    if entry:
        json_obj = entry_to_json(entry)
        json_obj["date_last_visit"] = history.date_last_visit
        json_obj["number_of_visits"] = history.visits

    return json_obj


def v_user_browse_history(request):
    context = {}
    context["query_page"] = "/json-user-browse-history"
    context["search_suggestions_page"] = None
    context["search_history_page"] = None
    javascript_list_utilities = get_template("javascript_list_utilities.js", context=context)

    context = {}
    context["javascript_list_utilities"] = javascript_list_utilities
    userbrowsehistory_list__script = get_template("userbrowsehistory_list__script.js", context=context)

    context = {}
    context["userbrowsehistory_list__script"] = userbrowsehistory_list__script
    thelist = get_template("userbrowsehistory_list.html", context=context)
    return get_html(id=0, body=thelist, title="Browse history")


def v_user_search_history(request):
    context = {}
    context["query_page"] = "/json-user-search-history"
    context["search_suggestions_page"] = None
    context["search_history_page"] = None
    javascript_list_utilities = get_template("javascript_list_utilities.js", context=context)

    context = {}
    context["javascript_list_utilities"] = javascript_list_utilities
    usersearchhistory_list__script = get_template("usersearchhistory_list__script.js", context=context)

    context = {}
    context["usersearchhistory_list__script"] = usersearchhistory_list__script
    thelist = get_template("usersearchhistory_list.html", context=context)
    return get_html(id=0, body=thelist, title="Search history")


def v_json_search_suggestions_entries(request):
    json_obj = [] # TODO
    return jsonify(json_obj)


def v_json_user_browse_history(request):
    json_obj = []

    c = Configuration.get_object()

    histories = c.model.filter(UserEntryVisitHistory, order_by=[desc(UserEntryVisitHistory.date_last_visit)], rows_per_page=50, page=1)

    for history in histories[:50]:
        json_data = browse_to_json(history)
        if json_data:
            json_obj.append(json_data)

    return jsonify(json_obj)


def v_json_user_search_history(request):
    json_obj = []

    c = Configuration.get_object()

    histories = c.model.filter(UserSearchHistory, order_by=[desc(UserSearchHistory.date)], rows_per_page=50, page=1)

    for history in histories[:50]:
        json_obj.append(search_history_to_json(history))

    return jsonify(json_obj)
