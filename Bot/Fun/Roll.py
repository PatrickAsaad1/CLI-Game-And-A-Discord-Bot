# Bot/Fun/Roll.py
import random
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="roll", aliases=["Roll", "ROLL", "dice", "Dice"])
    async def roll(ctx):
        logging.info(f"{ctx.author} used !roll command")
        result = random.randint(1, 6)
        await ctx.reply(f"🎲 You rolled a **{result}**!")
