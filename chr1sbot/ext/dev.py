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

import asyncio


class CodeblockConverter(commands.Converter):
    async def convert(self, ctx, argument):
        return argument # TODO

class Dev(commands.Cog, command_attrs=dict(hidden=True)):
    """Commands that only bot owners can use."""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def nick(self, ctx, *, new_nick=None):
        """Changes my nickname."""
        await ctx.me.edit(nick=new_nick)
        await ctx.send("Done.")

    @commands.command(aliases=["exec", "bash", "sh", "shell"])
    async def exec_(self, ctx, *, command):
        """Run commands in the system's default shell."""
        async with ctx.typing():
            proc = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
            try:
                stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=60.0)
                stdout = stdout.decode()
            except asyncio.TimeoutError:
                raise commands.CommandError("Command took longer than 60 seconds.")
            else:
                if len(stdout) > 1000:
                    await ctx.send(f"output: {await ctx.haste(stdout)}")
                else:
                    await ctx.send(f"```{stdout}```")

    @commands.command(aliases=["send", "echo"])
    async def say(self, ctx, *, content):
        await ctx.send(content)

    @commands.command(aliases=["clean"])
    async def cleanup(self, ctx, *, count: int=100):
        async for message in ctx.channel.history(limit=count):
            if message.author == ctx.me:
                try:
                    await message.delete()
                except:
                    pass
        await ctx.send(self.bot.emoji.get("check"))

    @commands.command()
    async def bean(self, ctx):
        raise ZeroDivisionError

def setup(bot):
    bot.add_cog(Dev(bot))
