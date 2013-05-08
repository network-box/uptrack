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


from sqlalchemy.types import TypeDecorator, Unicode

class Build(object):
    def __init__(self, name, epoch, version, release):
        self.name = unicode(name)
        self.evr = EVR(epoch, version, release)


class EVR(object):
    def __init__(self, epoch, version, release):
        self.epoch = unicode(epoch) if epoch is not None else u'0'
        self.version = unicode(version)
        self.release = unicode(release)

    def __str__(self):
        return "%s:%s-%s" % (self.epoch, self.version, self.release)

    # Note: The below (in)equality checking methods are naive: they don't know
    # about dist tags, they consider everything as string, not the way RPM
    # itself does.
    # Use them only if you are interested in strict (in)equality. Proper
    # comparison is done with rpm.labelCompare() as the 'uptodate' property of
    # our Package model.

    def __eq__(self, other):
        return (other is not None) and \
               (self.release == other.release) and \
               (self.version == other.version) and \
               (self.epoch == other.epoch)

    def __ne__(self, other):
        return not self.__eq__(other)


class EVRType(TypeDecorator):
    impl = Unicode

    def process_bind_param(self, evr, dialect):
        if evr is None:
            return evr

        return u"%s|%s|%s" % (evr.epoch, evr.version, evr.release)

    def process_result_value(self, value, dialect):
        if value is None:
            return value

        epoch, version, release = value.split("|")
        return EVR(epoch, version, release)


def dedist_release(release, dists):
    if ',' in dists:
        dists = [d.strip() for d in dists.split(',') if d]
    else:
        dists = [dists]

    for dist in dists:
        release = release.replace(dist, '')

    return release
