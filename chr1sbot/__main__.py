"""
chr1sBot Discord Bot
Copyright (C) 2020 chr1s

chr1sBot is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

chr1sBot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with chr1sBot. If not, see <https://www.gnu.org/licenses/>.
"""

import argparse

from chr1sbot import chr1sBot

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--beta", action="store_true", dest="beta", help="whether to use the beta account or not.")
parser.add_argument("-u", "--uvloop", action="store_true", dest="uvloop", help="whether to use uvloop or not. (requires linux)")
args = parser.parse_args()

if args.beta:
    import config_beta as config
else:
    import config

if args.uvloop:
    import uvloop
    uvloop.install()

chr1sBot(beta=args.beta, config=config).run(config.token)
