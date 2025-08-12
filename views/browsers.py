from flask import request, jsonify
from rsshistory.configuration import Configuration
from utils.controllers.browser import BrowserController
from utils.sqlmodel import Browser


def v_json_browsers(request):
    c = Configuration.get_object()

    browsers = c.model.all(Browser)

    data = {}
    data["browsers"] = []

    for browser in browsers:
        browser_controller = BrowserController(browser)
        data["browsers"].append(browser_controller.get_setup())

    return jsonify(data)
