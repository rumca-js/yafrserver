from utils.sqlmodel import (
    SqlModel,
    EntriesTable,
    EntriesTableController,
    SourcesTable,
    SourcesTableController,
    SourceOperationalData,
    SourceOperationalDataController,
)


class SourceDataBuilder(object):
    def __init__(self, conn, link=None, link_data=None, manual_entry=False):
        self.conn = conn
        self.link = link
        self.link_data = link_data

    def get_session(self):
        return self.conn.get_session()

    def build(self, link=None, link_data=None, manual_entry=False):
        if link_data:
            self.link_data = link_data
        if link:
            self.link = link

        if self.link_data:
            return self.build_from_props()
        elif self.link:
            return self.build_from_link()

    def build_from_link(self):
        rss_url = self.link

        if rss_url.endswith("/"):
            rss_url = rss_url[:-1]

        h = Url(rss_url)
        if not h.is_valid():
            return

        self.link_data = h.get_properties()

        return self.build_from_props()

    def is_source(self):
        Session = self.get_session()

        with Session() as session:
            count = (
                session.query(SourcesTable)
                .filter(SourcesTable.url == self.link_data["url"])
                .count()
            )
            if count != 0:
                return True

    def build_from_props(self):
        if self.is_source():
            return

        result = False

        Session = self.get_session()
        with Session() as session:
            table = SourcesTable(**self.link_data)

            session.add(table)
            session.commit()

            result = True

        return result

    def import_source(self, link_data=None):
        """
        importing might be different than building from scratch
        """
        self.build(link_data=link_data)
        print("import test")


def source_to_json(source, user_config=None):
    json_source = {}

    json_source["url_absolute"] = source.url
    json_source["url"] = source.url
    json_source["enabled"] = source.enabled
    json_source["source_type"] = source.source_type
    json_source["title"] = source.title
    json_source["category_name"] = source.category_name
    json_source["subcategory_name"] = source.subcategory_name
    json_source["export_to_cms"] = source.export_to_cms
    json_source["remove_after_days"] = source.remove_after_days
    json_source["language"] = source.language
    json_source["age"] = source.age
    json_source["favicon"] = source.favicon
    json_source["fetch_period"] = source.fetch_period
    json_source["auto_tag"] = source.auto_tag
    json_source["errors"] = 0

    return json_source
