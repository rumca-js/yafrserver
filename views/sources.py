from flask import request, jsonify
from utils.controllers.sources import source_to_json

from utils.controllers import (
    SourcesTableController,
)
from views.views import get_html
from rsshistory.configuration import Configuration


def v_sources(request):
    text = ""

    page = request.args.get("page") or ""
    search = request.args.get("search") or ""

    index = 0

    entry_id = request.args.get("id")
    link = f"/sources-json?page={page}&search={search}"

    text = """
    <div id="listData" class="container"></div>
    <div id="pagination" class="container"></div>
    <script>
       let loading_text = getSpinnerText();
       $('#listData').html(loading_text);
       $('#pagination').html(loading_text);

       getDynamicJson("{}", function(sources) {{
          let finished_text = getSourcesList(sources);
          let pagination_text = getPaginationText(sources, 200);
          $('#listData').html(finished_text);
          $('#pagination').html(pagination_text);
       }});
    </script>
    """.format(link)

    return get_html(id=0, body=text, title="Entries")


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
    text = ""

    link = request.args.get("link")
    id = request.args.get("source_id")

    c = Configuration.get_object()

    source = SourcesTableController(db = c.model).get(id=id)

    if source:
        text += """
        <div class="container">
                <img src="{}" width="100px" style="flex-shrink: 0;"/>
                <div>
                    <div>ID: {}</div>
                    <div>{}</div>
                    <div>{}</div>
                    <a href="/entries?source_id={}">Entries</a>
                </div>
        </div>
            """.format(source.favicon, source.id, source.title, source.url, source.id)
    else:
        text = "Not found"

    return get_html(id=0, body=text, title="Source")
