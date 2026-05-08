# Bot/ping.py
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="ping")
    async def ping(ctx):
        logging.info(f"Ping command by: {ctx.author}")
        await ctx.reply(f"🏓 Pong! {round(bot.latency * 1000)}ms")
