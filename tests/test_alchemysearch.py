from sqlalchemy import (
    create_engine,
)
from pathlib import Path

from utils import (
   SqlModel,
   EntriesTableController,
   EntriesTable,
   SourcesTable,
   SourcesTableController,
)
from utils.alchemysearch import AlchemySearch

import unittest


class AlchemySearchTest(unittest.TestCase):
    def setUp(self):
        self.found_row = None

    def create_table(self):
        self.engine = self.get_engine()

        self.db = SqlModel(database_file=self.get_engine_path(), engine=self.engine)

        controller = EntriesTableController(self.db)

        entry = {
                "title" : "Title",
                "link" : "https://title-in-head",
                "description" : "description",
        }

        controller.add_entry(entry)

    def handle_row(self, row):
        self.found_row = row

    def teardown(self):
        self.db = None

        path = Path(self.get_engine_path())
        if path.exists():
            print("Removed engine file")
            path.unlink()

    def get_engine_path(self):
        return "test_feedclient.db"

    def get_engine(self):
        return create_engine("sqlite:///" + self.get_engine_path())

    def test_search(self):
        self.teardown()

        self.create_table()

        test_link = "https://www.youtube.com/feeds/videos.xml?channel_id=UCXuqSBlHAE6Xw-yeJA0Tunw"

        search = AlchemySearch(self.engine, "link = https://title-in-head", self)
        search.search()

        self.assertTrue(self.found_row is not None)

        self.teardown()
