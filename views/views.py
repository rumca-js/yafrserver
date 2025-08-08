from rsshistory.status import Status
from rsshistory.configuration import Configuration

def get_navbar():
    text = """
    <nav id="navbar" class="navbar sticky-top navbar-expand-lg navbar-light bg-light">
      <div class="d-flex w-100">
        <!-- Form with search input -->
        <form action="/entries" method="get" class="d-flex w-100 ms-3" id="searchContainer" style="width: 60%;">
          <div class="input-group">
            <input id="searchInput" name="searchInput" class="form-control me-1 flex-grow-1" type="search" placeholder="Search" autofocus="" aria-label="Search">
            <button id="dropdownButton" class="btn btn-outline-secondary" type="button">⌄</button>
            <button id="searchButton" class="btn btn-outline-success" type="submit">🔍</button>
          </div>
        </form>

        <!-- Navbar toggler button, aligned to the right -->
        <button class="navbar-toggler ms-auto" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>
    
      <div class="collapse navbar-collapse ms-3" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a id="homeButton" class="nav-link" href="/">🏠</a>
          </li>

          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarViewDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              View
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarViewDropdown">
                <li><a id="viewStandard" class="dropdown-item" href="#">Standard</a></li>
                <li><a id="viewGallery" class="dropdown-item" href="#">Gallery</a></li>
                <li><a id="viewSearchEngine" class="dropdown-item" href="#">Search engine</a></li>

                <li><hr class="dropdown-divider"></li>

                <li><a id="displayLight" class="dropdown-item" href="#">Light</a></li>
                <li><a id="displayDark" class="dropdown-item" href="#">Dark</a></li>

                <li><hr class="dropdown-divider"></li>

                <li><a id="orderByVotes" class="dropdown-item" href="#">Order by Votes</a></li>
                <li><a id="orderByDatePublished" class="dropdown-item" href="#">Order by Date published</a></li>
            </ul>
          </li>

          <li class="nav-item">
            <a id="helpButton" class="nav-link" href="#">?</a>
          </li>
        </ul>
      </div>
    </nav>
    """

    return text



def get_html(id, body, title="", index=False):
    status = Status.get_object()
    c = Configuration.get_object()

    if not index:
        if not id:
            id = ""

    reading_entries_text = ""
    reading_sources_text = ""
    if status.reading_entries:
        reading_entries_text = f""" <div>Reading entries</div>"""
    if status.reading_sources:
        reading_sources_text = f""" <div>Reading sources</div>"""

    navbar_text = get_navbar()

    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/jszip/dist/jszip.min.js"></script>

        <link rel="stylesheet" href="/static/css/styles.css_style-light.css?1753905798">
        <script src="/static/library.js?=11"></script>
        <script src="/static/entries_library.js?=11"></script>
        <script src="/static/sources_library.js?=11"></script>
        <script src="/static/listview.js?=11"></script>

        <title>{title}</title>
    </head>
    <body style="padding-bottom: 6em;">

    {navbar_text}

    <div id="searchSuggestions"></div>

    {body}

    <footer id="footer" class="text-center text-lg-start bg-body-tertiary text-muted fixed-bottom">
      <div id="footerStatus" class="text-center p-1" style="display: block;">
        Version:{c.__version__}
        {reading_entries_text}
        {reading_sources_text}
      </div>
      <div id="footerLine" class="text-center p-1" style="display: none;background-color: rgba(0, 0, 0, 0);">
      </div>
    </footer>

    </body>
    </html>
    """

    return html
