# Bot/Fun/Coinflip.py
from Utils.Logger import setup_logging
import random

logging = setup_logging()


def setup(bot):
    @bot.command(
        name="coinflip",
        aliases=["Coin", "COIN", "coin", "COINFLIP", "Coinflip", "cf", "flip"],
    )
    async def coinflip(ctx):
        """Flip a coin and get heads or tails."""
        coin = random.choice(["Heads", "Tails"])
        logging.info(f"{ctx.author} flipped a coin: {coin}")
        await ctx.reply(f"🪙 The coin landed on **{coin}**!")
