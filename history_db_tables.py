# coding: utf-8
from sqlalchemy import Boolean, Column, Index, Integer, LargeBinary, String, Table, Text, text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

# sudo sqlacodegen sqlite:////home/$USER/.config/google-chrome/Default/History > history_db_tables.py

Base = declarative_base()
metadata = Base.metadata


class Download(Base):
    __tablename__ = 'downloads'

    id = Column(Integer, primary_key=True)
    guid = Column(String, nullable=False)
    current_path = Column(Text, nullable=False)
    target_path = Column(Text, nullable=False)
    start_time = Column(Integer, nullable=False)
    received_bytes = Column(Integer, nullable=False)
    total_bytes = Column(Integer, nullable=False)
    state = Column(Integer, nullable=False)
    danger_type = Column(Integer, nullable=False)
    interrupt_reason = Column(Integer, nullable=False)
    hash = Column(LargeBinary, nullable=False)
    end_time = Column(Integer, nullable=False)
    opened = Column(Integer, nullable=False)
    last_access_time = Column(Integer, nullable=False)
    transient = Column(Integer, nullable=False)
    referrer = Column(String, nullable=False)
    site_url = Column(String, nullable=False)
    tab_url = Column(String, nullable=False)
    tab_referrer_url = Column(String, nullable=False)
    http_method = Column(String, nullable=False)
    by_ext_id = Column(String, nullable=False)
    by_ext_name = Column(String, nullable=False)
    etag = Column(String, nullable=False)
    last_modified = Column(String, nullable=False)
    mime_type = Column(String(255), nullable=False)
    original_mime_type = Column(String(255), nullable=False)


class DownloadsSlice(Base):
    __tablename__ = 'downloads_slices'

    download_id = Column(Integer, primary_key=True, nullable=False)
    offset = Column(Integer, primary_key=True, nullable=False)
    received_bytes = Column(Integer, nullable=False)
    finished = Column(Integer, nullable=False, server_default=text("0"))


class DownloadsUrlChain(Base):
    __tablename__ = 'downloads_url_chains'

    id = Column(Integer, primary_key=True, nullable=False)
    chain_index = Column(Integer, primary_key=True, nullable=False)
    url = Column(Text, nullable=False)


t_keyword_search_terms = Table(
    'keyword_search_terms', metadata,
    Column('keyword_id', Integer, nullable=False),
    Column('url_id', Integer, nullable=False, index=True),
    Column('term', Text, nullable=False, index=True),
    Column('normalized_term', Text, nullable=False),
    Index('keyword_search_terms_index1', 'keyword_id', 'normalized_term')
)


class Meta(Base):
    __tablename__ = 'meta'

    key = Column(Text, primary_key=True, unique=True)
    value = Column(Text)


class SegmentUsage(Base):
    __tablename__ = 'segment_usage'
    __table_args__ = (
        Index('segment_usage_time_slot_segment_id', 'time_slot', 'segment_id'),
    )

    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, nullable=False, index=True)
    time_slot = Column(Integer, nullable=False)
    visit_count = Column(Integer, nullable=False, server_default=text("0"))


class Segment(Base):
    __tablename__ = 'segments'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    url_id = Column(Integer, index=True)


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class TypedUrlSyncMetadatum(Base):
    __tablename__ = 'typed_url_sync_metadata'

    storage_key = Column(Integer, primary_key=True)
    value = Column(LargeBinary)


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    url = Column(Text, index=True)
    title = Column(Text)
    visit_count = Column(Integer, nullable=False, server_default=text("0"))
    typed_count = Column(Integer, nullable=False, server_default=text("0"))
    last_visit_time = Column(Integer, nullable=False)
    hidden = Column(Integer, nullable=False, server_default=text("0"))


class VisitSource(Base):
    __tablename__ = 'visit_source'

    id = Column(Integer, primary_key=True)
    source = Column(Integer, nullable=False)


class Visit(Base):
    __tablename__ = 'visits'

    id = Column(Integer, primary_key=True)
    url = Column(Integer, nullable=False, index=True)
    visit_time = Column(Integer, nullable=False, index=True)
    from_visit = Column(Integer, index=True)
    transition = Column(Integer, nullable=False, server_default=text("0"))
    segment_id = Column(Integer)
    visit_duration = Column(Integer, nullable=False, server_default=text("0"))
    incremented_omnibox_typed_score = Column(Boolean, nullable=False, server_default=text("FALSE"))
    publicly_routable = Column(Boolean, nullable=False, server_default=text("FALSE"))
