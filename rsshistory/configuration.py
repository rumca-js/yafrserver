import os

from sqlalchemy import (
    create_engine,
)

from utils.sqlmodel import (
    SqlModel,
    ConfigurationEntryController,
)



class Configuration(object):
    obj = None

    def __init__(self):
        self.database_file_name = "feedclient.db"
        self.create_engine()
        self.set_server_location()

        self.config_entry = ConfigurationEntryController(db=self.model).get()

    def get_object():
        if not Configuration.obj:
            c = Configuration()
            Configuration.obj = c

        return Configuration.obj

    def create_engine(self):
        self.engine = create_engine("sqlite:///{}".format(self.database_file_name))
        self.model = SqlModel(database_file=self.database_file_name, engine=self.engine)

    def set_server_location(self):
        self.crawler_server = "127.0.0.1"
        if "CRAWLER_BUDDY_SERVER" in os.environ:
            self.crawler_server = os.environ["CRAWLER_BUDDY_SERVER"]
        crawler_port = "3000"
        if "CRAWLER_BUDDY_PORT" in os.environ:
            self.crawler_port = os.environ["CRAWLER_BUDDY_PORT"]

        self.crawler_location = f"http://{self.crawler_server}:{self.crawler_port}"
