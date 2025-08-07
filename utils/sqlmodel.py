"""
Library package.

Should be binary compatibile with django model

Right now we are not able to do sO.
"""

from typing import Optional
from sqlalchemy import (
    create_engine,
    Table,
    MetaData,
    select,
    func,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    delete,
    update,
)
from sqlalchemy.orm import sessionmaker
from datetime import timedelta, datetime, timezone

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .dateutils import DateUtils


def create_this_engine():
    file_name = "test.db"
    return create_engine("sqlite:///" + file_name)


class SqlConnection(object):
    """
    Simple wrapper for connection
    """

    def __init__(self, database_file="test.db", parser=None):
        self.cursor = None
        self.database_file = database_file

        self.parser = parser

        if not self.create_database():
            print("Could not connect to database")
            return

    def create_database(self):
        file_name = self.get_database_file()

        # try:

        # self.engine = create_engine('sqlite:///'+file_name, echo=True)
        self.engine = create_engine("sqlite:///" + file_name)
        return True

        # except Exception as e:
        #    print(
        #        "Could not create sqlite3 database file:{}. Exception:{}".format(
        #            file_name, str(e)
        #        )
        #    )
        #    return False

    def close(self):
        self.engine.dispose()

    def get_database_file(self):
        return self.database_file


class GenericTable(object):
    def __init__(self, sqlconnection):
        self.conn = sqlconnection

        self.table_name = None
        self.table = None

    def create(self):
        """
        Expected to set self.table
        """
        raise NotImplementedError(
            "GenericTable: create function has not been implemeneted"
        )

    def count(self):
        from sqlalchemy.sql import text

        st = select(func.count()).select_from(text(self.table_name))
        return self.get_connection().execute(st).scalar()

    def select(self):
        query = select(self.table)
        result = self.get_connection().execute(query)
        return result.fetchall()

    def truncate(self):
        if self.table_name:
            truncate_query = sqlalchemy.text("DELETE FROM {}".format(self.table_name))
            self.get_connection().execute(truncate_query)
            self.commit()

    def get_connection(self):
        return self.conn.conn

    def commit(self):
        self.conn.commit()


class Base(DeclarativeBase):
    pass


class EntriesTable(Base):
    __tablename__ = "linkdatamodel"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    link: Mapped[str] = mapped_column(String(30), unique=True)
    title: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    thumbnail: Mapped[Optional[str]]
    language: Mapped[Optional[str]]
    age: Mapped[int] = mapped_column(default=0)
    date_created = mapped_column(DateTime(timezone=True), nullable=True)
    date_published = mapped_column(DateTime(timezone=True), nullable=True)
    date_update_last = mapped_column(DateTime(timezone=True), nullable=True)
    date_dead_since = mapped_column(DateTime(timezone=True), nullable=True)
    date_last_modified = mapped_column(DateTime(timezone=True), nullable=True)
    status_code: Mapped[int] = mapped_column(default=0)
    page_rating: Mapped[int] = mapped_column(default=0)
    page_rating_votes: Mapped[int] = mapped_column(default=0)
    page_rating_contents: Mapped[int] = mapped_column(default=0)
    bookmarked: Mapped[bool] = mapped_column(default=False)
    permanent: Mapped[bool] = mapped_column(default=False)
    author: Mapped[Optional[str]]
    album: Mapped[Optional[str]]
    source_url: Mapped[Optional[str]]
    contents_type: Mapped[int] = mapped_column(default=0)
    page_rating_contents: Mapped[int] = mapped_column(default=0)
    page_rating_votes: Mapped[int] = mapped_column(default=0)
    page_rating_visits: Mapped[int] = mapped_column(default=0)
    page_rating: Mapped[int] = mapped_column(default=0)
    # advanced / foreign
    source_id: Mapped[Optional[int]]


class SourcesTable(Base):
    __tablename__ = "sourcedatamodel"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    enabled: Mapped[bool] = mapped_column(default=True)
    url: Mapped[str] = mapped_column(unique=True)
    title: Mapped[Optional[str]]
    age: Mapped[int] = mapped_column(default=0)
    category_id: Mapped[Optional[int]]
    subcategory_id: Mapped[Optional[int]]
    export_to_cms: Mapped[bool] = mapped_column(default=True)
    favicon: Mapped[Optional[str]]
    fetch_period: Mapped[Optional[int]]
    language: Mapped[Optional[str]]
    proxy_location: Mapped[Optional[str]]
    remove_after_days: Mapped[Optional[int]]
    source_type: Mapped[Optional[str]]
    category_name: Mapped[Optional[str]]
    subcategory_name: Mapped[Optional[str]]
    auto_tag: Mapped[str] = mapped_column(String(1000), default="")
    auto_update_favicon: Mapped[bool] = mapped_column(default=True)



class SourceOperationalData(Base):
    __tablename__ = "sourceoperationaldata"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_fetched = mapped_column(DateTime, nullable=True)
    source: Mapped[int]


class UserTags(Base):
    __tablename__ = "usertags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date = mapped_column(DateTime)
    tag: Mapped[str] = mapped_column(String(1000))

    entry_object: Mapped[Optional[int]]
    user_object: Mapped[Optional[int]]


class UserBookmarks(Base):
    __tablename__ = "userbookmarks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    date_bookmarked = mapped_column(DateTime)

    entry_object: Mapped[Optional[int]]
    user_object: Mapped[Optional[int]]


class UserVotes(Base):
    __tablename__ = "uservotes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user: Mapped[str] = mapped_column(String(1000))
    vote: Mapped[int] = mapped_column(default=0)

    entry_object: Mapped[Optional[int]]
    user_object: Mapped[Optional[int]]


class ReadMarkers(Base):
    __tablename__ = "readmarkers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    read_date = mapped_column(DateTime)
    source_object: Mapped[Optional[int]]

    def set(session, source=None):
        if not source:
            markers = session.query(ReadMarkers)
            if markers.count() == 0:
                m = ReadMarkers(read_date=DateUtils.get_datetime_now_utc())
                session.add(m)
                session.commit()
            else:
                marker = markers.first()
                marker.read_date = DateUtils.get_datetime_now_utc()
                session.commit()
        else:
            markers = session.query(ReadMarkers, source_object == source.id)
            if markers.count() == 0:
                m = ReadMarkers(
                    read_date=DateUtils.get_datetime_now_utc(), source_object=source.id
                )
                session.add(m)
                session.commit()
            else:
                marker = markers.first()
                marker.read_date = DateUtils.get_datetime_now_utc()
                session.commit()


class ConfigurationEntry(Base):
    __tablename__ = "configurationentry"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    instance_title: Mapped[str] = mapped_column(String(500))
    instance_description: Mapped[Optional[str]] = mapped_column(String(500))
    instance_internet_location: Mapped[Optional[str]] = mapped_column(String(200))
    favicon_internet_url: Mapped[Optional[str]] = mapped_column(String(200))
    admin_user: Mapped[Optional[str]] = mapped_column(String(500))
    view_access_type: Mapped[Optional[str]] = mapped_column(String(100))
    download_access_type: Mapped[Optional[str]] = mapped_column(String(100))
    add_access_type: Mapped[Optional[str]] = mapped_column(String(100))
    logging_level: Mapped[int] = mapped_column(default=0)
    initialized: Mapped[bool] = mapped_column(default=False)
    initialization_type: Mapped[Optional[str]] = mapped_column(String(100))
    enable_background_jobs: Mapped[bool] = mapped_column(default=True)
    block_job_queue: Mapped[bool] = mapped_column(default=False)
    use_internal_scripts: Mapped[bool] = mapped_column(default=False)
    data_import_path: Mapped[Optional[str]] = mapped_column(String(2000))
    data_export_path: Mapped[Optional[str]] = mapped_column(String(2000))
    download_path: Mapped[Optional[str]] = mapped_column(String(2000))
    auto_store_thumbnails: Mapped[bool] = mapped_column(default=False)
    thread_memory_threshold: Mapped[int] = mapped_column(default=0)
    enable_keyword_support: Mapped[bool] = mapped_column(default=False)
    enable_domain_support: Mapped[bool] = mapped_column(default=False)
    enable_file_support: Mapped[bool] = mapped_column(default=False)
    enable_link_archiving: Mapped[bool] = mapped_column(default=False)
    enable_source_archiving: Mapped[bool] = mapped_column(default=False)

    accept_dead_links: Mapped[bool] = mapped_column(default=False)
    accept_ip_links: Mapped[bool] = mapped_column(default=False)
    accept_domain_links: Mapped[bool] = mapped_column(default=False)
    accept_non_domain_links: Mapped[bool] = mapped_column(default=False)
    auto_scan_new_entries: Mapped[bool] = mapped_column(default=False)
    new_entries_merge_data: Mapped[bool] = mapped_column(default=False)
    new_entries_use_clean_data: Mapped[bool] = mapped_column(default=False)
    entry_update_via_internet: Mapped[bool] = mapped_column(default=False)
    log_remove_entries: Mapped[bool] = mapped_column(default=False)
    auto_create_sources: Mapped[bool] = mapped_column(default=False)
    default_source_state: Mapped[bool] = mapped_column(default=False)
    prefer_https_links: Mapped[bool] = mapped_column(default=False)
    prefer_https_links: Mapped[bool] = mapped_column(default=False)
    prefer_non_www_links: Mapped[bool] = mapped_column(default=False)

    sources_refresh_period: Mapped[int] = mapped_column(default=0)
    days_to_move_to_archive: Mapped[int] = mapped_column(default=0)
    days_to_remove_links: Mapped[int] = mapped_column(default=0)
    days_to_remove_stale_entries: Mapped[int] = mapped_column(default=0)
    days_to_check_std_entries: Mapped[int] = mapped_column(default=0)
    days_to_check_stale_entries: Mapped[int] = mapped_column(default=0)
    remove_entry_vote_threshold: Mapped[int] = mapped_column(default=1)
    number_of_update_entries: Mapped[int] = mapped_column(default=1)

    remote_webtools_server_location: Mapped[Optional[str]] = mapped_column(default="")
    internet_status_test_url: Mapped[Optional[str]] = mapped_column(default="https://google.com")

    track_user_actions: Mapped[bool] = mapped_column(default=False)
    track_user_searches: Mapped[bool] = mapped_column(default=False)
    track_user_navigation: Mapped[bool] = mapped_column(default=False)
    max_user_entry_visit_history: Mapped[int] = mapped_column(default=1)
    max_number_of_user_search: Mapped[int] = mapped_column(default=1)
    vote_min: Mapped[int] = mapped_column(default=-100)
    vote_max: Mapped[int] = mapped_column(default=-100)
    number_of_comments_per_day: Mapped[int] = mapped_column(default=-100)

    time_zone: Mapped[int] = mapped_column(default=-100)
    display_style: Mapped[int] = mapped_column(default=-100)
    display_type: Mapped[int] = mapped_column(default=-100)
    show_icons: Mapped[bool] = mapped_column(default=False)
    thumbnails_as_icons: Mapped[bool] = mapped_column(default=False)
    small_icons: Mapped[bool] = mapped_column(default=False)
    local_icons: Mapped[bool] = mapped_column(default=False)
    links_per_page: Mapped[int] = mapped_column(default=-100)
    sources_per_page: Mapped[int] = mapped_column(default=-100)
    max_links_per_page: Mapped[int] = mapped_column(default=-100)
    max_sources_per_page: Mapped[int] = mapped_column(default=-100)
    max_number_of_related_links: Mapped[int] = mapped_column(default=-100)
    debug_mode: Mapped[bool] = mapped_column(default=False)


class SqlModel(object):
    def __init__(self, database_file="test.db", parser=None, engine=None):
        self.db_file = database_file

        if not engine:
            self.engine = create_engine("sqlite:///" + self.db_file)
        else:
            self.engine = engine

        Base.metadata.create_all(self.engine)

    def get_session(self):
        _SessionFactory = sessionmaker(bind=self.engine)
        return _SessionFactory

    def close(self):
        if self.engine:
            self.engine.dispose()
