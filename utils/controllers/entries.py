from rsshistory.webtools import Url

from utils.sqlmodel import (
    SqlModel,
    EntriesTable,
    EntriesTableController,
    SourcesTable,
    SourcesTableController,
    SourceOperationalData,
    SourceOperationalDataController,
)


class EntryWrapper(object):
    def __init__(self, entry=None, link=None):
        self.entry = entry
        self.link = link

    def get(self):
        pass

    def move_from_archive(self, entry):
        pass

    def move_to_archive(self, entry):
        pass

    def get_clean_data(data):
        return data


class EntryDataBuilder(object):
    def __init__(
        self,
        conn,
        link=None,
        link_data=None,
        manual_entry=False,
        allow_recursion=True,
        ignore_errors=False,
    ):
        self.conn = conn
        self.link = link
        self.link_data = link_data

    def get_session(self):
        return self.conn.get_session()

    def build(
        self,
        link=None,
        link_data=None,
        manual_entry=False,
        allow_recursion=True,
        ignore_errors=False,
    ):
        if link:
            self.link = link
        if link_data:
            self.link_data = link_data

        if self.link_data:
            self.build_from_props()
        elif self.link:
            self.build_from_link()

    def build_from_link(self):
        rss_url = self.link

        if rss_url.endswith("/"):
            rss_url = rss_url[:-1]

        h = Url(rss_url)
        if not h.is_valid():
            return

        self.link_data = h.get_properties()

        return self.build_from_props()

    def build_from_props(self):
        Session = self.get_session()
        with Session() as session:
            table = EntriesTable(**self.link_data)

            session.add(table)
            session.commit()

    def import_entry(self, link_data=None, source_is_auto=False):
        """
        importing might be different than building from scratch
        """
        pass
        print("test")


def entry_to_json(entry, user_config=None, tags=False):
    json_entry = {}
    json_entry["id"] = entry.id

    user_inappropate = False

    if user_config:
        user_inappropate = (
            entry.age != 0 and entry.age != None and entry.age > user_config.get_age()
        )
    else:
        user_inappropate = (
            entry.age != 0 and entry.age != None
        )

    if user_inappropate:
        json_entry["title"] = "Not appropriate"
    else:
        json_entry["title"] = entry.title

    if user_inappropate:
        json_entry["title_safe"] = "Not appropriate"
    else:
        json_entry["title_safe"] = entry.get_title_safe()

    if user_inappropate:
        json_entry["description"] = "Not appropriate"
    else:
        json_entry["description"] = entry.description

    if user_inappropate:
        json_entry["description_safe"] = "Not appropriate"
    else:
        json_entry["description_safe"] = entry.get_description_safe()
    json_entry["link"] = entry.link
    json_entry["link_absolute"] = entry.get_absolute_url()
    json_entry["is_valid"] = entry.is_valid()
    json_entry["date_created"] = entry.date_created
    json_entry["date_published"] = entry.date_published
    json_entry["date_dead_since"] = entry.date_dead_since
    json_entry["date_update_last"] = entry.date_update_last
    json_entry["date_last_modified"] = entry.date_last_modified
    json_entry["bookmarked"] = entry.bookmarked
    json_entry["permanent"] = entry.permanent
    json_entry["author"] = entry.author
    json_entry["album"] = entry.album
    json_entry["page_rating_contents"] = entry.page_rating_contents
    json_entry["page_rating_votes"] = entry.page_rating_votes
    json_entry["age"] = entry.age

    json_entry["source__title"] = ""
    json_entry["source__url"] = ""

    if hasattr(entry, "source"):
        if entry.source:
            json_entry["source__title"] = entry.source.title
            json_entry["source__url"] = entry.source.url

    if user_config and user_config.show_icons:
        if user_inappropate:
            json_entry["thumbnail"] = None
        else:
            if user_config.thumbnails_as_icons:
                json_entry["thumbnail"] = entry.get_thumbnail()
            else:
                json_entry["thumbnail"] = entry.get_favicon()

    if hasattr(entry, "tags"):
        tags = set()
        if entry.tags:
            for tag in entry.tags.all():
                tags.add(tag.tag)

        json_entry["tags"] = list(tags)

    return json_entry
