from rsshistory.configuration import Configuration
from utils.controllers.browser import BrowserController
from utils.sqlmodel import Browser
from rsshistory.webtools import (
   RemoteServer,
)


def get_properties_with_browser(request):
    link = request.args.get("link") or ""

    browser = get_request_browser(request)
    if browser:
        browser_controller = BrowserController(browser)
        browser_data = browser_controller.get_setup()
    else:
        browser_data = None

    html = request.args.get("html") or None

    if html:
        if browser_data:
            browser_data["settings"]["handler_class"] = "HttpPageHandler"   # TODO should not be hardcoded?
        else:
            browser_data={}
            browser_data["settings"] = {}
            if html:
                browser_data["settings"]["handler_class"] = "HttpPageHandler"

    c = Configuration.get_object()
    remote_server = RemoteServer(c.crawler_location)
    if not remote_server.is_ok():
        return

    all_properties = remote_server.get_getj(link, settings = browser_data)
    return all_properties


def get_request_browser_id(request):
    id = request.args.get("browser") or None
    return id


def get_request_browser(request):
    browser_id = get_request_browser_id(request)
    if browser_id:
        c = Configuration.get_object()
        browser = c.model.get(Browser, browser_id)
        return browser


def get_template(name, context=None):
    with open("static/templates/" + name) as fh:
        data = fh.read()
        if context:
            for item in context:
                value = context[item]
                key = "{"+item+ "}"
                if value is None:
                    value = ""
                else:
                    value = str(value)
                data = data.replace(key, value)

        return data


def get_navbar():
    return get_template("base_menu.html")


def get_header():
    c = Configuration.get_object()
    user_config = c.config_entry

    title = user_config.instance_title

    context = {}
    context["user_config.display_style"] = user_config.display_style
    context["user_config.display_type"] = user_config.display_type

    context["user_config.show_icons"] = user_config.show_icons
    context["user_config.small_icons"] = user_config.small_icons
    context["debug"] = user_config.debug_mode
    context["user_config.get_age"] = 18

    base_script = get_template("base_script.js", context=context)

    context = {}
    context["title"] = title
    context["base_script"] = base_script

    return get_template("base_head.html", context=context)


def get_footer():
    c = Configuration.get_object()
    version = c.__version__
    context = {}
    context["__version__"] = version
    return get_template("base_footer.html", context=context)



def get_html(id, body, title="", index=False):
    c = Configuration.get_object()

    if not index:
        if not id:
            id = ""

    navbar_text = get_navbar()
    base_head = get_header()
    footer_text = get_footer()

    html = f"""<!DOCTYPE html>
    <html>
    <head>
       {base_head}
    </head>
    <body style="padding-bottom: 6em;">
       {navbar_text}

       {body}

       {footer_text}

    </body>
    </html>
    """

    return html
