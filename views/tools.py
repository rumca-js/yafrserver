from flask import request, jsonify
from collections import OrderedDict
from views.views import get_html, get_template, get_properties_with_browser
from rsshistory.configuration import Configuration
from rsshistory.webtools import (
   RemoteServer,
)


def get_page_errors(link):
    notes = []
    warnings = []
    errors = []

    location = UrlLocation(link)
    domain = location.get_domain()

    if domain.lower() != domain:
        warnings.append("Link domain is not lowercase. Are you sure link name is OK?")
    if link.find("?") >= 0:
        warnings.append("Link contains arguments. Is that intentional?")
    if link.find("#") >= 0:
        warnings.append("Link contains arguments. Is that intentional?")
    if location.get_port() and location.get_port() >= 0:
        warnings.append("Link contains port. Is that intentional?")
    if not location.is_web_link():
        warnings.append("Not a web link. Expecting protocol://domain.tld styled location")

    if not location.is_protocolled_link():
        errors.append("Not a protocolled link. Is that intentional?")

    result = {}
    result["notes"] = notes
    result["warnings"] = warnings
    result["errors"] = errors

    return result


def v_json_page_props(request):
    link = request.args.get("link") or ""

    if link == "":
        data = {}
        data["status"] = False
        data["errors"] = ["Link in not in arguments"]
        return jsonify(data)

    c = Configuration.get_object()
    remote_server = RemoteServer(c.crawler_location)
    if not remote_server.is_ok():
        data = {}
        data["status"] = False
        data["errors"] = ["Remote server is down"]
        return jsonify(data)

    all_properties = get_properties_with_browser(request)

    if not all_properties:
        data = OrderedDict()
        data["properties"] = all_properties
        data["status"] = False
        data["errors"] = ["Could not obtain properties"]
        return jsonify(data)

    for item in all_properties:
        if item["name"] == "Response":
            if "data" in item:
                if "hash" in item["data"]:
                    item["data"]["body_hash"] = str(item["data"]["body_hash"])
                    item["data"]["hash"] = str(item["data"]["hash"])

    data = OrderedDict()
    data["properties"] = all_properties
    data["status"] = True

    # data["errors"] = get_errors(url_ex) TODO

    return jsonify(data)


def v_page_show_props(request):
    page_show_props__script = get_template("page_show_props__script.js")

    context = {}
    context["page_show_props__script"] = page_show_props__script

    page_show_props = get_template("page_show_props.html", context=context)
    return get_html(id=0, body=page_show_props, title="Page properties")
