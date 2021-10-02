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

import time

import discord
from discord.ext import commands, menus
import async_cse


class Google(commands.Cog):
    """Commands for searching things on Google."""

    def __init__(self, bot):
        self.bot = bot
        self.google = async_cse.Search(self.bot.keychain.get("google"))

    def cog_unload(self):
        self.bot.loop.create_task(self.google.close())

    def _gen_embeds(self, ctx, responses, footer, images):
        """Generate the embed list for ext.menus"""
        embeds = list()
        for resp in responses:
            embed = discord.Embed(
                title=resp.title,
                description=resp.description,
                colour=self.bot.color,
                url=resp.url,
            )
            if images:
                embed.set_image(url=resp.image_url)
            else:
                if resp.image_url != resp.url:
                    embed.set_thumbnail(url=resp.image_url)
            fmt = f"Result {responses.index(resp)}/{len(responses)-1}"
            embed.set_footer(text=f"{fmt} | {footer}")
            embeds.append(embed)
        return embeds

    async def _do_google(self, ctx, query, images):
        """Auxiliary function for searching"""
        start = time.time()
        if ctx.channel.is_nsfw():
            safesearch = "off"
            resp = await self.google.search(query, safesearch=False, image_search=images)
        else:
            safesearch = "on"
            resp = await self.google.search(query, safesearch=True, image_search=images)
        end = time.time()
        footer = f"{end - start:.2f}s | SafeSearch is {safesearch}"
        return self._gen_embeds(ctx, resp, footer, images)

    async def _handle_paging(self, ctx, query, *, images):
        embeds = await self._do_google(ctx, query, images=images)
        pages = menus.MenuPages(source=GoogleMenuSource(range(1, 10), embeds), delete_message_after=True)
        await pages.start(ctx)

    @commands.group(name="google", invoke_without_command=True, aliases=["g", "search"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _google(self, ctx, *, query: str):
        """Uses Google to search for stuff."""
        await self._handle_paging(ctx, query, images=False)

    @_google.command(aliases=["i", "pic"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def image(self, ctx, *, query: str):
        """Uses Google to search for images."""
        await self._handle_paging(ctx, query, images=True)


class GoogleMenuSource(menus.ListPageSource):
    def __init__(self, data, embeds):
        self.data = data
        self.embeds = embeds
        super().__init__(data, per_page=1)

    async def format_page(self, menu, entries):
        return self.embeds[entries]


def setup(bot):
    """Adds the cog"""
    bot.add_cog(Google(bot))
