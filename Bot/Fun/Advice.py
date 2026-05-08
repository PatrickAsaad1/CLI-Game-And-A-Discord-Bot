# Bot/Fun/Advice.py
import requests
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="advice", aliases=["Advice", "ADVICE"])
    async def advice(ctx):
        """Get a random piece of advice."""
        try:
            response = requests.get("https://api.adviceslip.com/advice")
            json_data = response.json()
            advice_text = json_data["slip"]["advice"]
            await ctx.reply(f"💡 **{advice_text}**")
            logging.info(f"{ctx.author} used !advice and got: {advice_text}")
        except Exception as e:
            logging.error(f"Advice API error: {e}")
            await ctx.reply("❌ Could not fetch advice right now. Try again later!")
