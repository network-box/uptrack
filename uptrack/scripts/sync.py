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


import argparse
import os
import sys

from sqlalchemy import engine_from_config

from pyramid.paster import get_appsettings, setup_logging

from uptrack.models import DBSession
from uptrack.sync import Sync


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--distro", "-d", default=None,
                        help="The distro to synchronize (all by default)")
    parser.add_argument("config", help="The Uptrack configuration file")

    return parser.parse_args()

def main():
    args = get_args()
    config_uri = args.config

    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    sync = Sync(settings)
    sync.run(distro_name=args.distro)
