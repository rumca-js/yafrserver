let small_icons = true;

function getSourceListText(source) {
    let source_link = `/source?source_id=${source.id}`;
    let hover_title = source.title;
    let invalid_style = "";
    let bookmark_class = "";
    let thumbnail_text = "";
    if (source.favicon) {
       const iconClass = small_icons ? 'icon-small' : 'icon-normal';
       thumbnail_text = `<img src="${source.favicon}" class="${iconClass}"/>`;
    }
    let title_safe = source.title;

    return `
        <a 
            href="${source_link}"
            source="${source.id}"
            title="${hover_title}"
            ${invalid_style}
            class="my-1 p-1 list-group-item list-group-item-action ${bookmark_class} border rounded"
        >
            <div class="d-flex">
                ${thumbnail_text}
                <div class="mx-2">
                    <span style="font-weight:bold" class="text-reset">${title_safe}</span>
                    <div class="text-reset">
                        ${source.title}
                    </div>
                </div>
            </div>
        </a>
    `;
}


function getSourcesList(sources) {
    let htmlOutput = '';

    htmlOutput = `  <span class="container list-group">`;

    if (view_display_type == "gallery") {
        htmlOutput += `  <span class="d-flex flex-wrap">`;
    }

    if (sources && sources.length > 0) {
        sources.forEach((source) => {
            const listItem = getSourceListText(source);

            if (listItem) {
                htmlOutput += listItem;
            }
        });
    } else {
        htmlOutput = '<li class="list-group-item">No sources found</li>';
    }

    if (view_display_type == "gallery") {
        htmlOutput += `</span>`;
    }

    htmlOutput += `</span>`;

    return htmlOutput;
}
