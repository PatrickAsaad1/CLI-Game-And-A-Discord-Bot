# Bot/Utilities/QR.py
import requests
from Utils.Logger import setup_logging
import asyncio

logging = setup_logging()


def setup(bot):
    @bot.command(name="qr", aliases=["Qr", "QR", "qrcode"])
    async def qr(ctx, *, text):
        logging.info(f"{ctx.author} chose to generate a QR code")
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={text}"
        await ctx.reply(qr_url)
        logging.info(f"QR code generated for: {text}")
