# Bot_games/guess.py
import random
import asyncio
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="guess", aliases=["Guess", "GUESS"])
    async def Guess(ctx):
        logging.info(f"User {ctx.author} started Guess The Number game.")

        score = 0
        difficulty_ranges = {
            "easy": (1, 3),
            "med": (1, 5),
            "medium": (1, 5),
            "hard": (1, 10),
        }

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.reply("Choose difficulty: `easy`, `med`, or `hard`")

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            game = msg.content.lower()
        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up!")
            return

        if game == "quit":
            await ctx.reply("👋 Game cancelled!")
            return

        if game not in difficulty_ranges:
            await ctx.reply("❌ Invalid! Choose: easy, med, or hard")
            return

        low, high = difficulty_ranges[game]
        await ctx.reply(
            f"Great! I'll pick a number between {low} and {high}\n"
            f"Try to reach 3 points to win! Type `quit` to stop."
        )

        while score < 3:
            rnum = random.randint(low, high)
            await ctx.reply(f"\n🎯 Guess a number ({low}-{high}):")

            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                user_input = msg.content.lower()
            except asyncio.TimeoutError:
                await ctx.send("⏰ Time's up!")
                return

            if user_input == "quit":
                await ctx.reply("👋 Game cancelled!")
                return

            try:
                unum = int(user_input)
            except ValueError:
                await ctx.reply("❌ Please enter a number!")
                continue

            if unum < low or unum > high:
                await ctx.reply(f"❌ Enter a number between {low} and {high}!")
                continue

            await ctx.send(f"The number was: **{rnum}**")

            if unum == rnum:
                await ctx.reply("✅ You got it right! +1 point!")
                score += 1
                logging.info(f"User guessed correctly. Score: {score}/3")
            else:
                await ctx.reply("❌ Wrong guess!")
                if score > 0:
                    score -= 1
                logging.info(f"User guessed incorrectly. Score: {score}/3")

            await ctx.reply(f"📊 Your score: **{score}/3**")

        await ctx.reply("🎉🎉🎉 **YOU WON! Reached 3 points!** 🎉🎉🎉")
        logging.info(f"User {ctx.author} won the guessing game!")

        await ctx.send("\nPlay again? (yes/no)")
        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.lower() in ["yes", "y"]:
                await Guess(ctx)
            else:
                await ctx.send("Thanks for playing!")
        except asyncio.TimeoutError:
            await ctx.send("Thanks for playing!")
