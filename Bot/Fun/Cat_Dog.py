# Bot/Fun/Animals.py
import requests
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="cat", aliases=["Cat", "CAT", "kitty", "meow"])
    async def Cat(ctx):
        logging.info(f"{ctx.author} used !cat command")
        try:
            response = requests.get(
                "https://api.thecatapi.com/v1/images/search", timeout=30.0
            )
            data = response.json()
            await ctx.reply(data[0]["url"])
            logging.info(f"Cat pic was sent to {ctx.author}")
        except:
            await ctx.reply("Couldn't get a cat pic, try again later!")
            logging.error("Cat API error")

    @bot.command(name="dog", aliases=["Dog", "DOG"])
    async def Dog(ctx):
        logging.info(f"{ctx.author} used !dog command")
        try:
            response = requests.get("https://dog.ceo/api/breeds/image/random")
            data = response.json()
            await ctx.reply(data["message"])
            logging.info(f"Dog pic was sent to {ctx.author}")
        except:
            await ctx.reply("Couldn't get a dog pic, try again later!")
            logging.error("Dog API error")
