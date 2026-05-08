# Bot/Fun/Joke.py
import requests
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(
        name="joke",
        aliases=["Joke", "JOKE", "DADJOKE", "DadJoke", "Dadjoke", "dadjoke"],
    )
    async def joke(ctx):
        logging.info(f"{ctx.author} used !joke command")
        try:
            headers = {"Accept": "application/json"}
            response = requests.get("https://icanhazdadjoke.com/", headers=headers)
            json_data = response.json()
            await ctx.reply(f"😂 **{json_data['joke']}**")
            logging.info("Joke sent successfully")
        except:
            await ctx.reply("❌ Couldn't fetch a joke right now. Try again later!")
            logging.error("Joke API error")
