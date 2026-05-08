# Bot/Fun/Meme.py
import requests
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="meme", aliases=["Meme", "MEME"])
    async def meme(ctx):
        logging.info(f"{ctx.author} used !meme command")
        try:
            response = requests.get("https://meme-api.com/gimme")
            json_data = response.json()
            await ctx.reply(json_data["url"])
            logging.info(f"Meme sent from r/{json_data['subreddit']}")
        except Exception as e:
            logging.error(f"Meme API error: {e}")
            await ctx.reply("❌ Could not fetch a meme right now. Try again later!")
