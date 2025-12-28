# +++ Modified By Yato [telegram username: @i_killed_my_clan & @ProYato] +++
import asyncio
import os
from datetime import datetime

from pyrogram import Client
from pyrogram.enums import ParseMode
import pyrogram.utils

from aiohttp import web
from config import API_HASH, APP_ID, LOGGER, TG_BOT_WORKERS, PORT, OWNER_ID
from plugins import web_server

# IMPORTANT: Prevent invalid channel ID bug
pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

name = """
Links Sharing Started
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="linkshare_bot_session",   # ✅ FIX 1: stable session name
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=os.environ.get("TG_BOT_TOKEN"),  # ✅ FIX 2: env variable
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.uptime = datetime.now()
        self.username = me.username

        # Notify owner
        try:
            await self.send_message(
                OWNER_ID,
                "<b><blockquote>🤖 Bot Restarted ♻️</blockquote></b>",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            self.LOGGER(__name__).warning(f"Owner notify failed: {e}")

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info("Bot Running Successfully ✅")
        self.LOGGER(__name__).info(name)

        # Web server (Render health check)
        try:
            app = web.AppRunner(await web_server())
            await app.setup()
            await web.TCPSite(app, "0.0.0.0", PORT).start()
            self.LOGGER(__name__).info(f"Web server running on port {PORT}")
        except Exception as e:
            self.LOGGER(__name__).error(f"Web server error: {e}")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

# Broadcast cancel helpers
is_canceled = False
cancel_lock = asyncio.Lock()

if __name__ == "__main__":
    Bot().run()
