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

import traceback
import sys

import discord
from discord.ext import commands
from sentry_sdk import configure_scope, capture_exception


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return
        if isinstance(error, commands.CommandNotFound):
            return
        error = getattr(error, "original", error)

        if isinstance(error, commands.CommandOnCooldown):
            if await self.bot.is_owner(ctx.author):
                return await ctx.reinvoke()
            else:
                return await ctx.send(f"You are on cooldown. Try again in {error.retry_after:.2f} seconds.")

        elif isinstance(error, self.bot.config.handled_errors):
            return await ctx.send(repr(error))

        else:
            with configure_scope() as scope:
                scope.user = {"id": ctx.author.id, "username": str(ctx.author)}
                scope.set_tag("message_id", ctx.message.id)
                scope.set_tag("guild_id", ctx.guild.id)
                scope.set_tag("channel_id", ctx.channel.id)

                capture_exception(error)

            return await ctx.send(repr(error))

    @commands.Cog.listener()
    async def on_error(self, error, *args, **kwargs):
        capture_exception(error)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
