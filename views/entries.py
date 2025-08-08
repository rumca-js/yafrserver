from flask import request, jsonify

from rsshistory.configuration import Configuration
from utils.alchemysearch import AlchemySearch
from views.views import get_html
from utils.controllers.entries import entry_to_json

from utils.controllers import (
    EntriesTableController,
)


def v_entries(request):
    text = ""

    link = request.args.get("link") or ""
    source_id = request.args.get("source_id")
    page = request.args.get("page") or ""
    search = request.args.get("search") or ""

    index = 0

    entry_id = request.args.get("id")
    link = f"/entries-json?link={link}&page={page}&source_id={source_id}&search={search}"

    text = """
    <div id="listData" class="container"></div>
    <div id="pagination" class="container"></div>
    <script>
       let loading_text = getSpinnerText();
       $('#listData').html(loading_text);

       getDynamicJson("{}", function(entries) {{
          let finished_text = getEntriesList(entries);
          let pagination_text = getPaginationText(entries, 200);
          $('#listData').html(finished_text);
          $('#pagination').html(pagination_text);
       }});
    </script>
    """.format(link)

    return get_html(id=0, body=text, title="Entries")


def v_entries_json(request):
    c = Configuration.get_object()

    link = request.args.get("link") or None
    search = request.args.get("search") or None
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

    text = """
    <div class="container">
       <div id="entryData"></div>
    </div>

    <script>
        let loading_text = getSpinnerText();
        $('#entryData').html(loading_text);

        getDynamicJson("{}", function(entry) {{
            var finished_text = getEntryDetailText(entry);
            $('#entryData').html(finished_text);

            document.title = entry.title;
        }});
        getDislikeData(1, entry_id={});
    </script>
    """.format(link, id)

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
