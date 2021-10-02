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

import discord
from discord.ext import commands, menus, tasks

import asyncio
import functools
import contextlib


class chr1sBotContext(commands.Context):
    """Custom context class for a few helpers"""

    async def react(self, emoji):
        """Shorthand for ctx.message.add_reaction"""
        await self.message.add_reaction(emoji)

    async def haste(self, content, *, raw=True):
        """
        Posts stuff to my personal hastebin server.
        You can actually just use your own by changing `config.haste_url`
        """
        resp = await self.bot.session.post(f"{self.bot.config.haste_url}/documents", data=content.encode("utf-8"))
        key = (await resp.json())["key"]
        return self.bot.config.haste_url + (f"/raw/{key}" if raw else f"/{key}")
