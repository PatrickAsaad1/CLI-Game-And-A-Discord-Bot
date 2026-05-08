# Bot/Quotes.py
import requests
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="quote", aliases=["Quotes", "QUOTES", "QUOTE", "Quote"])
    async def quote(ctx):
        """Loads a random quote from the ZenQuotes API."""
        try:
            response = requests.get("https://zenquotes.io/api/random")
            json_data = response.json()
            await ctx.reply(f"✨ {json_data[0]['q']} — *{json_data[0]['a']}*")

            logging.info(
                f"{ctx.author} used !quote and got: {json_data[0]['q'][:50]}..."
            )

        except Exception as e:
            logging.error(f"Quote API error: {e}")
            await ctx.reply("❌ Could not fetch a quote right now. Try again later!")
