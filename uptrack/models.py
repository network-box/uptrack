# Copyright (c) 2013 - Network Box
#
# This file is part of Uptrack.
#
# Uptrack is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Uptrack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Uptrack.  If not, see <http://www.gnu.org/licenses/>.


from bcrypt import gensalt, hashpw

from rpm import labelCompare as compareEVRs

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, scoped_session, sessionmaker
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Text, Unicode

from zope.sqlalchemy import ZopeTransactionExtension

from uptrack.utils import EVRType, dedist_release


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class BaseModel(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __json__(self, request=None):
        d = {}

        for c in self.__table__.columns:
            attr = c.name

            if "password" in attr:
                continue

            value = getattr(self, attr)

            if value is None:
                value = ''

            if hasattr(value, "encode"):
                value = value.encode("utf-8")

            d[attr] = value

        return d


class Package(Base, BaseModel):
    __tablename__ = 'packages'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    distro_id = Column(Integer, ForeignKey('distros.id'), nullable=False)
    evr = Column(EVRType)
    upstream_id = Column(Integer, ForeignKey('upstreams.id'))
    upstream_evr = Column(EVRType)

    distro = relation("Distro", backref="packages")
    upstream = relation("Upstream", backref="packages")

    def __str__(self):
        if self.evr is None:
            return self.name

        return "%s-%s" % (self.name, self.evr)

    @property
    def uptodate(self):
        if self.upstream_evr is None:
            raise ValueError("We don't know the package's upstream EVR")

        release = dedist_release(self.evr.release,
                                 self.distro.dist_tags)
        up_release = dedist_release(self.upstream_evr.release,
                                    self.upstream.dist_tags)

        fresh = compareEVRs((self.evr.epoch,
                             self.evr.version,
                             release),
                            (self.upstream_evr.epoch,
                             self.upstream_evr.version,
                             up_release))

        if fresh == 0:
            return True

        if fresh == -1:
            return False

        if fresh == 1:
            raise ValueError("The evr of our package is newer than upstream")

        raise ValueError("Comparing this package's EVR and upstream EVR "
                         "returned '%s'" % fresh)


class Distro(Base, BaseModel):
    __tablename__ = 'distros'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True, nullable=False)
    koji_tag = Column(Unicode, unique=True, nullable=False)
    git_branch = Column(Unicode, unique=True, nullable=False)
    dist_tags = Column(Unicode, nullable=False)
    upstream_id = Column(Integer, ForeignKey('upstreams.id'))

    upstream = relation("Upstream")


class Upstream(Base, BaseModel):
    __tablename__ = 'upstreams'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True, nullable=False)
    git_branch = Column(Unicode, unique=True, nullable=False)
    base_url = Column(Unicode, unique=True, nullable=False)
    dist_tags = Column(Unicode, nullable=False)

    def __str__(self):
        return self.name


class User(Base, BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(Unicode, unique=True, nullable=False)
    email = Column(Unicode, unique=True)
    __password = Column('password', Text, nullable=False)
    name = Column(Unicode)

    def __get_password(self):
        return self.__password

    def __set_password(self, password):
        self.__password = hashpw(password, gensalt())

    password = property(__get_password, __set_password)

    def validate_password(self, password):
        return hashpw(password, self.__password) == self.__password
