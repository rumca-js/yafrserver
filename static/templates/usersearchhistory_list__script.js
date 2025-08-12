
function getRowsList(queue) {
    let htmlOutput = '';

    if (queue && queue.length > 0) {
        queue.forEach(entry => {
           htmlOutput += getEntryVisitsBar(entry);
        });
    }

    return htmlOutput;
}


{javascript_list_utilities}
