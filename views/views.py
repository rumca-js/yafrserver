from rsshistory.configuration import Configuration


def get_template(name, context=None):
    with open("static/templates/" + name) as fh:
        data = fh.read()
        if context:
            for item in context:
                value = context[item]
                key = "{"+item+ "}"
                data = data.replace(key, value)

        return data


def get_navbar():
    return get_template("base_menu.html")


def get_header():
    c = Configuration.get_object()
    title = c.config_entry.instance_title
    context = {}
    context["title"] = title

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
