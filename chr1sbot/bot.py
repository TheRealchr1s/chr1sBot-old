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
import aiohttp
import asyncpg
import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

import sys
import os
import asyncio
import logging
import traceback

from .utils import chr1sBotContext

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_RETAIN"] = "True"

# set up logging
formatting = "[%(asctime)s] [%(levelname)s:%(name)s] %(message)s"
logger = logging.getLogger(__name__)
discord_logger = logging.getLogger("discord")
discord_logger.setLevel(logging.INFO)
logging.basicConfig(format=formatting, level=logging.INFO)

handler = logging.FileHandler(filename="logs/discord.log", encoding="utf-8", mode="w")
bot_handler = logging.FileHandler(filename="logs/chr1sbot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter(formatting))
bot_handler.setFormatter(logging.Formatter(formatting))

discord_logger.addHandler(handler)
logger.addHandler(bot_handler)


class chr1sBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        beta = kwargs.pop("beta")
        config = kwargs.pop("config")
        super().__init__(command_prefix=commands.when_mentioned_or(*config.prefixes), **kwargs)
        self.logger = logger
        self.beta = beta
        self.config = config
        self.color = self.config.color
        self.keychain = self.config.keychain
        self.emoji = self.config.emojis
        self.first_on_ready = True
        self.allowed_mentions = discord.AllowedMentions(everyone=False, roles=False)
        self.activity = discord.Activity(name="your beans", type=discord.ActivityType.watching)
        self.sentry = sentry_sdk.init(dsn=self.config.sentry_dsn, integrations=[AioHttpIntegration()])

    async def on_ready(self):
        if self.first_on_ready:
            self.session = aiohttp.ClientSession(loop=self.loop)
            self.webhook = discord.Webhook.from_url(self.config.error_hook, adapter=discord.AsyncWebhookAdapter(self.session))
            self.logger.info("Bot is ready.")
            self.logger.info("I am in %s guilds.", len(self.guilds))
            await self._load_extensions()
            await self._init_connections()
            self.first_on_ready = False
        else:
            self.logger.info("Ignoring READY.")

    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild:
            return
        await self.invoke(await self.get_context(message, cls=chr1sBotContext))

    async def on_message_edit(self, before, after):
        if before.content != after.content:
            ctx = await self.get_context(after, cls=chr1sBotContext)
            await self.invoke(ctx)

    async def _init_connections(self):
        self.db = await asyncpg.create_pool(self.config.psql_dsn)
        self.logger.info("Connected to Postgres.")

    async def _load_extensions(self):
        for ext in self.config.extensions:
            try:
                self.load_extension(ext)
            except BaseException:
                self.logger.critical(f"Extension {ext} couldn't be loaded. Traceback:\n\n{traceback.format_exc()}")
            else:
                self.logger.info(f"Loaded {ext}.")

    async def close(self):
        [task.cancel() for task in asyncio.all_tasks(loop=self.loop)]
        await self.session.close()
        await super().close()
