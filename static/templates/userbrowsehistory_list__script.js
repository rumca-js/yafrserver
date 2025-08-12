function getEntryVisitsBar(entry) {
    let link_absolute = getEntryLink(entry);
    let id = entry.id;
    let title = entry.title;
    let title_safe = getEntryTitleSafe(entry);
    let link = entry.link;
    let thumbnail = entry.thumbnail;
    let source__title = entry.source__title;
    let date_published = getEntryDatePublished(entry);
    let date_last_visit = entry.date_last_visit.toLocaleString();
    let number_of_visits = entry.number_of_visits;

    let badge_text = getEntryVotesBadge(entry, true);
    let badge_star = getEntryBookmarkBadge(entry, true);
    let badge_age = getEntryAgeBadge(entry, true);
    let badge_dead = getEntryDeadBadge(entry, true);

    let img_text = '';
    if (view_show_icons) {
        const iconClass = view_small_icons ? 'icon-small' : 'icon-normal';
        img_text = `<img src="${thumbnail}" class="rounded ${iconClass}" />`;
    }
    let link_text = getEntryLinkText(entry);

    let text = `
         <a
         class="list-group-item list-group-item-action"
         href="${link_absolute}" title="${title}">
             ${badge_text}
             ${badge_star}
             ${badge_age}
             ${badge_dead}

             <div class="d-flex">
               ${img_text}

               <div class="mx-2">
                  ${title_safe}
                  Visits:${number_of_visits}
                  Date of the last visit:${date_last_visit}
		  ${link_text}
               </div>
             </div>
         </a>
    `;
    return text;
}


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
