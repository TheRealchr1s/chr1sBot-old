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
from discord.ext import commands

from collections import Counter


class Meta(commands.Cog):
    """Things regarding the bot itself."""

    def __init__(self, bot):
        self.bot = bot
        
        if not hasattr(bot, "socket_stats"):
            bot.socket_stats = Counter()

    @commands.command(aliases=["src"])
    async def source(self, ctx):
        """Shows the bot's source code."""
        await ctx.send("https://github.com/TheRealchr1s/chr1sBot")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.bot.logger.info("{0.author} ({0.author.id}) used {0.command} in {0.guild} ({0.guild.id})".format(ctx))

    @commands.command(aliases=["pong"])
    async def ping(self, ctx):
        """Yes"""
        await ctx.send("No thanks.")

    @commands.Cog.listener()
    async def on_socket_response(self, msg):
        self.bot.socket_stats[msg.get("t")] += 1


def setup(bot):
    bot.add_cog(Meta(bot))
