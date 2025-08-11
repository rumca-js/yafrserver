import os

from sqlalchemy import (
    create_engine,
)

from utils.sqlmodel import (
    SqlModel,
)
from utils.controllers import (
    ConfigurationEntryController,
)


class Configuration(object):
    obj = None

    def __init__(self):
        self.database_file_name = "feedclient.db"

        # increment major version digit for releases, or link name changes
        # increment minor version digit for JSON data changes
        # increment last digit for small changes
        self.__version__ = "6.0.0"

        self.entries_per_page = 200

        self.create_engine()
        self.set_server_location()

        controller = ConfigurationEntryController(db=self.model)
        self.config_entry = controller.get()
        if not self.config_entry:
            config = {}
            config["instance_title"] = "Instance"
            config["instance_description"] = "Instance"
            controller.add(config)
            self.config_entry = controller.get()


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
        self.crawler_server = "192.168.0.200"
        if "CRAWLER_BUDDY_SERVER" in os.environ:
            self.crawler_server = os.environ["CRAWLER_BUDDY_SERVER"]
        self.crawler_port = "3000"
        if "CRAWLER_BUDDY_PORT" in os.environ:
            self.crawler_port = os.environ["CRAWLER_BUDDY_PORT"]

        self.crawler_location = f"http://{self.crawler_server}:{self.crawler_port}"
