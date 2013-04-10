from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Release(Base):
    __tablename__ = 'release'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True, nullable=False)
    koji_tag = Column(Unicode, unique=True, nullable=False)
    git_url = Column(Unicode, unique=True, nullable=False)

    def __init__(self, name=None, koji_tag=None, git_url=None):
        self.name = name
        self.koji_tag = koji_tag
        self.git_url = git_url
