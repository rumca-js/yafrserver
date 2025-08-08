import time
import json
from utils.controllers.sources import SourceDataBuilder
from rsshistory.status import Status
from rsshistory.configuration import Configuration
from rsshistory.webtools import (
   RemoteServer,
)
from utils.controllers.sourcesreader import SourceReader

c = Configuration()


def fetch(url):
    request_server = RemoteServer(c.crawler_location)

    all_properties = request_server.get_getj(url)
    return all_properties


def read_sources(file):
    with open(file, "r") as fh:
        contents = fh.read()
        return json.loads(contents)


def process():
    status = Status.get_object()

    print("-----Reading sources-----")

    news_sources = read_sources("init_sources_news.json")
    status.reading_sources = True
    for key, source in enumerate(news_sources):
        builder = SourceDataBuilder(conn=c.model)
        source["id"] = key
        try:
            source_obj = builder.build(link_data = source)
            if source_obj:
                print("Built {}".format(source["url"]))
        except Exception as E:
            print(str(E))
    status.reading_sources = False

    remote_server = RemoteServer(c.crawler_location)
    print("-----Starting operation-----")

    reader = SourceReader(db = c.model)
    
    while True:
        print("In a loop")
        if remote_server.is_ok():
            status.reading_entries = True
            reader.read()
            status.reading_entries = False
        else:
            print(f"Server is not OK {c.crawler_location}")

        time.sleep(60*10) # every 10 minutes
