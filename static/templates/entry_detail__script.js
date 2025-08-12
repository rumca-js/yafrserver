let loading_text = getSpinnerText();
$('#entryData').html(loading_text);

getDynamicJson("{link}", function(entry) {
    var finished_text = getEntryDetailText(entry);
    $('#entryData').html(finished_text);

    document.title = entry.title;
});
getDislikeData(1, entry_id={entry_id});
