let search_suggestions = [];
let default_page_size = 200;
let user_age = 0;

let view_display_type = "standard";
let view_show_icons = true;
let view_small_icons = false;
let show_pure_links = false;
let highlight_bookmarks = false;
let sort_function = "-date_published"; // page_rating_votes, date_published



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


function performSearch() {
    const search_text = $("#searchInput").val();
    let page_num = parseInt(getQueryParam("page")) || 1;
    let page_size = default_page_size;

    let link = `/entries-json?page=${page_num}&search=${search_text}`;

    getDynamicJson(link, function(entries) {{
        var finished_text = getEntriesList(entries);
        let pagination_text = getPaginationText(entries, 200);
        $('#listData').html(finished_text);
        $('#pagination').html(pagination_text);
    }});
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
document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing")
    $("#searchSuggestions").html(getSearchSuggestionContainer());
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

