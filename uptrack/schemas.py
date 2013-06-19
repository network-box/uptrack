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


import colander
import deform

from uptrack.models import DBSession, Upstream


def get_upstream_options():
    yield ('', '--')
    for upstream in DBSession.query(Upstream):
        yield (upstream.id, upstream.name)

def upstream_validator(node, upstream_id):
    for id, name in get_upstream_options():
        if upstream_id == id:
            return None

    raise colander.Invalid("Please choose a valid upstream")

@colander.deferred
def deferred_upstream_widget(node, kw):
    return deform.widget.SelectWidget(values=get_upstream_options())


class DistroSchema(colander.Schema):
    id = colander.SchemaNode(colander.Integer(),
                             widget=deform.widget.HiddenWidget(),
                             missing=colander.null)
    name = colander.SchemaNode(colander.String())
    koji_tag = colander.SchemaNode(colander.String())
    dist_tags = colander.SchemaNode(colander.String())
    downstream_prefix = colander.SchemaNode(colander.String())

# This is unused, don't expose it for now, to avoid confusing Herlo :)
#    git_branch = colander.SchemaNode(colander.String(), missing=colander.null)
    upstream_id = colander.SchemaNode(colander.Integer(), title="Upstream",
                                      widget=deferred_upstream_widget,
                                      missing=colander.null,
                                      validator=upstream_validator)


class UpstreamSchema(colander.Schema):
    id = colander.SchemaNode(colander.Integer(),
                             widget=deform.widget.HiddenWidget(),
                             missing=colander.null)
    name = colander.SchemaNode(colander.String())
    dist_tags = colander.SchemaNode(colander.String())
    base_urls = colander.SchemaNode(colander.String(), title="Base URLs")

# This is unused, don't expose it for now, to avoid confusing Herlo :)
#    git_branch = colander.SchemaNode(colander.String(), missing=colander.null)


class UserSchema(colander.Schema):
    id = colander.SchemaNode(colander.Integer(),
                             widget=deform.widget.HiddenWidget(),
                             missing=colander.null)
    login = colander.SchemaNode(colander.String())
    name = colander.SchemaNode(colander.String())
    email = colander.SchemaNode(colander.String())
    password = colander.SchemaNode(colander.String(),
                                   widget=deform.widget.PasswordWidget())
