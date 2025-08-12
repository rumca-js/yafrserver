from flask import request, jsonify

from rsshistory.configuration import Configuration
from utils.alchemysearch import AlchemySearch
from views.views import get_html, get_template
from utils.controllers.entries import entry_to_json

from utils.controllers import (
    EntriesTableController,
)
from rsshistory.webtools import (
   RemoteServer,
)


def v_entries(request):
    text = ""

    page = request.args.get("page") or ""
    search = request.args.get("search") or ""
    view = request.args.get("view") or ""

    form_action_url = "/entries"
    form_method = "GET"
    form_submit_button_name = "Search"

    context = {}
    context["query_page"] = "/entries-json"
    context["search_suggestions_page"] = "/json-search-suggestions-entries"
    context["search_history_page"] = "/json-user-search-history"
    javascript_list_utilities = get_template("javascript_list_utilities.js", context=context)

    context = {}
    context["query_page"] = "/entries-json"
    context["search_suggestions_page"] = "/json-search-suggestions-entries"
    context["search_history_page"] = "/json-user-search-history"
    context["javascript_list_utilities"] = javascript_list_utilities
    entries_list__script = get_template("entry_list__script.js", context = context)

    context = {}
    context["form_action_url"] = form_action_url
    context["form_method"] = form_method
    context["form_submit_button_name"] = form_submit_button_name
    context["entries_list__script"] = entries_list__script

    entries_list = get_template("entry_list.html", context = context)

    return get_html(id=0, body=entries_list, title="Entries")


def v_entries_json(request):
    c = Configuration.get_object()

    link = request.args.get("link") or None
    search = request.args.get("search") or None
    view = request.args.get("view") or None
    source_id = request.args.get("source_id")
    if source_id == "None":
        source_id = None
    if source_id:
        source_id = int(source_id)
    page = request.args.get("page") or 1
    page = int(page)

    entries_json = []

    search_engine = AlchemySearch(db=c.engine, page=page, rows_per_page=c.entries_per_page, search_term=search, ascending=False)
    entries = search_engine.get_filtered_objects()

    for entry in reversed(entries):
        entry_json = entry_to_json(entry)

        entries_json.append(entry_json)

    return jsonify(entries_json)


def v_entry(request):
    id = request.args.get("entry_id")

    link = f"/entry-json?entry_id={id}"

    context = {}
    context["link"] = link
    entry_detail__script = get_template("entry_detail__script.js", context=context)

    context = {}
    context["entry_detail__script"] = entry_detail__script
    text = get_template("entry_detail.html", context=context)

    return get_html(id=0, body=text, title="Entries")


def v_entry_json(request):
    c = Configuration.get_object()

    link = request.args.get("link")
    id = request.args.get("entry_id")

    entry_json = {}

    entry = EntriesTableController(db = c.model).get(id=id)
    if entry:
        entry_json = entry_to_json(entry)

    return jsonify(entry_json)


def v_entry_dislikes(request):
    text = ""
    c = Configuration.get_object()

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
