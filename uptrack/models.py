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

from sqlalchemy import Column, Integer, Text, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class BaseModel(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __json__(self, request=None):
        d = {}

        for attr in self._sa_class_manager.keys():
            if "password" in attr:
                continue

            value = getattr(self, attr)

            if value is None:
                value = ''

            if hasattr(value, "encode"):
                value = value.encode("utf-8")

            d[attr] = value

        return d

class Release(Base, BaseModel):
    __tablename__ = 'releases'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True, nullable=False)
    koji_tag = Column(Unicode, unique=True, nullable=False)
    git_url = Column(Unicode, unique=True, nullable=False)


class Upstream(Base, BaseModel):
    __tablename__ = 'upstreams'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True, nullable=False)
    base_url = Column(Unicode, unique=True, nullable=False)


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
