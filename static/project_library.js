let view_display_type = "standard";
let view_show_icons = true;
let view_small_icons = false;
let show_pure_links = false;
let highlight_bookmarks = false;
let user_age = 0;

let search_suggestions = [];
let default_page_size = 200;
let sort_fuction="-date_published";
let common_indicators = null;

let debug = false;


function add_text(error_line, text) {
    let result = "";
    if (error_line == "") {
        result = text;
    }
    else {
        result += ", " + text;
    }

    return result;
}


function setDisplayMode() {
    if (view_display_style == "style-light") {
       setLightMode();

       let icons = document.querySelectorAll('.mainbutton-icon');
       
       icons.forEach(icon => {
           icon.style.filter = "";
       });

       icons = document.querySelectorAll('.content-icon');
       
       icons.forEach(icon => {
           icon.style.filter = "";
       });
    }
    if (view_display_style == "style-dark") {
       setDarkMode();

       let icons = document.querySelectorAll('.mainbutton-icon');
       
       icons.forEach(icon => {
           icon.style.filter = 'invert(1)';
       });

       icons = document.querySelectorAll('.content-icon');
       
       icons.forEach(icon => {
           icon.style.filter = 'invert(1)';
       });
    }
}


function setLightMode() {
    view_display_style = "style-light";

    const linkElement = document.querySelector('link[rel="stylesheet"][href*="styles.css_style-"]');
    if (linkElement) {
        // TODO replace rsshistory with something else
        //linkElement.href = "/django/rsshistory/css/styles.css_style-light.css";
    }

    const htmlElement = document.documentElement;
    htmlElement.setAttribute("data-bs-theme", "light");

    const navbar = document.getElementById('navbar');
    navbar.classList.remove('navbar-light', 'bg-dark');
    navbar.classList.add('navbar-dark', 'bg-light');
}


function setDarkMode() {
    view_display_style = "style-dark";

    const linkElement = document.querySelector('link[rel="stylesheet"][href*="styles.css_style-"]');
    if (linkElement) {
        //linkElement.href = "/django/rsshistory/css/styles.css_style-dark.css";
    }

    const htmlElement = document.documentElement;
    htmlElement.setAttribute("data-bs-theme", "dark");

    const navbar = document.getElementById('navbar');
    navbar.classList.remove('navbar-light', 'bg-light');
    navbar.classList.add('navbar-dark', 'bg-dark');
}



function getInitialSearchSuggestsions() {
   return ["link=*youtube.com/channel*",
        "link=*github.com/*",
        "link=*reddit.com/*",
   ];
}


function getSearchSuggestsions() {
   let initial_search_suggestions = getInitialSearchSuggestsions();

   return [...search_suggestions, ...initial_search_suggestions];
}


function getSearchSuggestionContainer() {
    const suggestions = getSearchSuggestsions();
    let listItems = suggestions.map(suggestion =>
        `<li class="list-group-item suggestion-item" data-search="${suggestion}">🔍${suggestion}</li>`
    ).join("");

    let html = `
        <div id="search-suggestions" class="mt-2" style="display:none;">
            <ul class="list-group" id="suggestion-list">
               ${listItems}
            </ul>
        </div>
    `;
    return html;
}


function getPaginationText(rows, page_size) {
    let page_num = parseInt(getQueryParam("page")) || 1;
    let countElements = rows.length;

    if (countElements == 0)
    {
       return "";
    }

    return GetPaginationNavSimple(page_num);
}


function hideSearchSuggestions() {
   let search_suggestions = document.getElementById("search-suggestions");
   search_suggestions.style.display = "none";
   $("#dropdownButton").html("⌄");
}


function showSearchSuggestions() {
   let search_suggestions = document.getElementById("search-suggestions");
   search_suggestions.style.display = "block";
   $("#dropdownButton").html("^");
}


let currentgetDislikeData = 0;
function getDislikeData(attempt = 1, entry_id=null) {
    let requestgetDislikeData = ++currentgetDislikeData;
    let url_address = `/entry-dislikes?entry_id=${entry_id}`;

    $.ajax({
       url: url_address,
       type: 'GET',
       timeout: 10000,
       success: function(data) {
           if (requestgetDislikeData != currentgetDislikeData) {
               return;
           }
           if (data) {
               entry_dislike_data = data;
               fillDislike();
           }
       },
       error: function(xhr, status, error) {
           if (requestgetDislikeData != currentgetDislikeData) {
               return;
           }
           if (attempt < 3) {
               getDislikeData(attempt + 1);
           } else {
           }
       }
    });
}

let currentgetIndicators = 0;
function getIndicators(attempt=1) {
    let requestCurrentgetIndicators = ++currentgetIndicators;

    let url = '/json-indicators';
    
    $.ajax({
       url: url,
       type: 'GET',
       timeout: 10000,
       success: function(data) {
           if (requestCurrentgetIndicators != currentgetIndicators)
           {
               return;
           }
           common_indicators = data.indicators;

           SetMenuStatusLine();
           SetFooterStatusLine();
       },
       error: function(xhr, status, error) {
           if (requestCurrentgetIndicators != currentgetIndicators)
           {
               return;
           }
           
           if (attempt < 3) {
               getIndicators(attempt + 1);
           } else {
           }
       }
    });
}


function SetMenuStatusLine() {
       if (common_indicators.read_later_queue.status) {
           showElement(".readLaterElement");
       }
       else {
           hideElement(".readLaterElement");
       }
       if (common_indicators.sources_error.status) {
           showElement(".sourceErrorElement");
       }
       else {
           hideElement(".sourceErrorElement");
       }
       if (common_indicators.threads_error.status) {
           showElement(".configurationErrorElement");
       }
       else {
           hideElement(".configurationErrorElement");
       }
       if (common_indicators.configuration_error.status ||
           common_indicators.jobs_error.status) {
           showElement(".adminErrorElement");
       }
       else {
           hideElement(".adminErrorElement");
       }
}


function SetFooterStatusLine() {
   let error_line = "";

   if (common_indicators.sources_error.status) {
       error_line += add_text(error_line, "Sources");
   }
   if (common_indicators.threads_error.status) {
       error_line += add_text(error_line, "Threads");
   }
   if (common_indicators.jobs_error.status) {
       error_line += add_text(error_line, "Jobs");
   }
   if (common_indicators.configuration_error.status) {
       error_line += add_text(error_line, "Configuration");
   }
   if (common_indicators.internet_error.status) {
       error_line += add_text(error_line, "Internet");
   }
   if (common_indicators.crawling_server_error.status) {
       error_line += add_text(error_line, "Crawling server");
   }
   if (common_indicators.is_reading.status) {
       error_line += add_text(error_line, common_indicators.is_reading.message);
   }

   if (error_line == "") {
       $("#footerLine").html("");
       $("#footerLine").hide();
   }
   else {
       $("#footerLine").html(error_line);
       $("#footerLine").show();
   }
}


function fillDislike() {
    let parameters = $('#entryParameters').html();

    let { thumbs_up, thumbs_down, view_count, upvote_ratio, upvote_view_ratio } = entry_dislike_data;

    let text = [];

    if (thumbs_up) text.push(`<div class="text-nowrap mx-1">👍${getHumanReadableNumber(thumbs_up)}</div>`);
    if (thumbs_down) text.push(`<div class="text-nowrap mx-1">👎${getHumanReadableNumber(thumbs_down)}</div>`);
    if (view_count) text.push(`<div class="text-nowrap mx-1">👁${getHumanReadableNumber(view_count)}</div>`);

    if (upvote_ratio) text.push(`<div class="text-nowrap mx-1">👍/👎${parseFloat(upvote_ratio).toFixed(2)}</div>`);
    if (upvote_view_ratio) text.push(`<div class="text-nowrap mx-1">👍/👁${parseFloat(upvote_view_ratio).toFixed(2)}</div>`);

    parameters = `${parameters} ${text.join(" ")}`;

    $('#entryParameters').html(parameters);
}


function processMenuData(data, container) {
    let finished_text = `
    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
       ${data.title}
    </a>
    <ul class="dropdown-menu">
        `;


    let style_text = "";
    if (view_display_style == "style-dark") {
        style_text = "filter:invert(1)";
    }

    data.rows.forEach(row => {

       finished_text += `
       <li>
         <a href="${row.link}" class="dropdown-item" title="${row.title}">
           <img src="${row.icon}" class="mainbutton-icon" style="${style_text}"/>
           ${row.title}
         </a>
       </li>
       `;
    });

    finished_text += "</ul>"

    $(container).html(finished_text);
}


function getMenuSearchContainer() {
    let link = "json-search-container";
    getDynamicJson(link, function(data) {
        processMenuData(data, '#MenuSearchContainer');
    });
}


function getMenuGlobalContainer() {
    let link = "json-global-container";
    getDynamicJson(link, function(data) {
        processMenuData(data, '#MenuGlobalContainer');
    });
}


function getMenuPersonalContainer() {
    let link = "json-personal-container";
    getDynamicJson(link, function(data) {
        processMenuData(data, '#MenuPersonalContainer');
    });
}


function getMenuTools() {
    let link = "json-tools-container";
    getDynamicJson(link, function(data) {
        processMenuData(data, '#MenuToolsContainer');
    });
}


function getMenuUsers() {
    let link = "json-users-container";
    getDynamicJson(link, function(data) {
        processMenuData(data, '#MenuUsersContainer');
    });
}


function performSearch() {
    const search_text = $("#searchInput").val();
    let page_num = parseInt(getQueryParam("page")) || 1;
    let page_size = default_page_size;

    let link = `/entries-json?page=${page_num}&search=${search_text}`;

    getDynamicJson(link, function(entries) {
        var finished_text = getEntriesList(entries);
        let pagination_text = getPaginationText(entries, 200);
        $('#listData').html(finished_text);
        $('#pagination').html(pagination_text);
    });
}


function getBasicPageElements() {
    getIndicators();
    getMenuSearchContainer();
    getMenuGlobalContainer();
    getMenuPersonalContainer();
    getMenuTools();
    getMenuUsers();
}


//-----------------------------------------------
$(document).on('click', '.btnNavigation', function(e) {
    e.preventDefault();

    const currentPage = $(this).data('page');

    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('page', currentPage);
    window.history.pushState({}, '', currentUrl);

    animateToTop();

    performSearch();
});


//-----------------------------------------------
$(document).on('keydown', "#searchInput", function(e) {
    if (e.key === "Enter") {
        e.preventDefault();

        hideSearchSuggestions();

        performSearch();
    }
});


//-----------------------------------------------
$(document).on('click', '.suggestion-item', function(e) {
    e.preventDefault();

    const searchInput = document.getElementById('searchInput');
    let suggestion_item_value = $(this).data('search')

    searchInput.value = suggestion_item_value;

    hideSearchSuggestions();

    performSearch();
});


//-----------------------------------------------
$(document).on('click', '#dropdownButton', function(e) {
    e.preventDefault();

    let search_suggestions = document.getElementById("search-suggestions");
    if (search_suggestions.style.display == "none") {
        showSearchSuggestions();
    }
    else {
        hideSearchSuggestions();
    }
});
