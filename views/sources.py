from flask import request, jsonify
from utils.controllers.sources import source_to_json

from utils.controllers import (
    SourcesTableController,
)
from views.views import get_html, get_template
from rsshistory.configuration import Configuration


def v_sources(request):
    text = ""

    page = request.args.get("page") or ""
    search = request.args.get("search") or ""

    form_action_url = "/entries"
    form_method = "GET"
    form_submit_button_name = "Search"

    context = {}
    context["query_page"] = "/sources-json"
    context["search_suggestions_page"] = None
    context["search_history_page"] = None
    javascript_list_utilities = get_template("javascript_list_utilities.js", context=context)

    context = {}
    context["query_page"] = "/sources-json"
    context["search_suggestions_page"] = None
    context["search_history_page"] = None
    context["javascript_list_utilities"] = javascript_list_utilities
    source_list__script = get_template("source_list__script.js", context = context)

    context = {}
    context["form_action_url"] = form_action_url
    context["form_method"] = form_method
    context["form_submit_button_name"] = form_submit_button_name
    context["source_list__script"] = source_list__script

    source_list = get_template("source_list.html", context = context)

    return get_html(id=0, body=source_list, title="Sources")


def v_sources_json(request):
    text = ""
    c = Configuration.get_object()

    link = request.args.get("link")
    page = request.args.get("page") or 1
    page=int(page)

    sources_json = []

    sources = SourcesTableController(db=c.model).filter(page=page, rows_per_page=c.entries_per_page)
    sources_size = len(sources)
    for source in sources:
        source_json = source_to_json(source)
        sources_json.append(source_json)

    return jsonify(sources_json)


def v_source(request):

    link = request.args.get("link")
    id = request.args.get("source_id")

    c = Configuration.get_object()

    source = SourcesTableController(db = c.model).get(id=id)

    if source:
        source_text = f"""
                <img src="{source.favicon}" width="100px" style="flex-shrink: 0;"/>
                <div>
                    <div>ID: {source.id}</div>
                    <div>{source.title}</div>
                    <div>{source.url}</div>
                    <a href="/entries?source_id={source.id}">Entries</a>
                </div>
            """
    else:
        source_text = "Not found"

    context={}
    context["source_text"] = source_text
    source_detail = get_template("source_detail.html", context=context)

    return get_html(id=0, body=source_detail, title="Source")
