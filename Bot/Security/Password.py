# games/password_generator.py
from Utils.Logger import setup_logging
import random
import asyncio

logging = setup_logging()


def setup(bot):
    @bot.command(name="passgen", aliases=["password", "genpass", "bgen"])
    async def password_gen(ctx):
        """Generate random passwords."""
        logging.info(f"{ctx.author} selected password generator")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.reply(
            "🔢 How many passwords do you want to generate? (Max: 10, type `quit` to cancel)"
        )

        while True:
            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                if msg.content.lower() == "quit":
                    await ctx.reply("👋 Cancelled!")
                    return

                if not msg.content.isdigit():
                    await ctx.reply("❌ Please enter a valid number! (Max: 10)")
                    continue

                manypass = int(msg.content)

                if manypass <= 0:
                    await ctx.reply("❌ Number must be positive!")
                    continue

                if manypass > 10:
                    await ctx.reply("❌ Maximum is 10 passwords!")
                    continue

                break

            except asyncio.TimeoutError:
                await ctx.send("⏰ Time's up! Cancelled.")
                return

        logging.info(f"{ctx.author} wants to generate {manypass} passwords")

        await ctx.send(
            "📏 How many characters per password? (Max: 50, type `quit` to cancel)"
        )

        while True:
            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                if msg.content.lower() == "quit":
                    await ctx.reply("👋 Cancelled!")
                    return

                if not msg.content.isdigit():
                    await ctx.reply("❌ Please enter a valid number!")
                    continue

                manychar = int(msg.content)

                if manychar < 4:
                    await ctx.reply("❌ Password must be at least 4 characters!")
                    continue

                if manychar > 50:
                    await ctx.reply("❌ Maximum is 50 characters!")
                    continue

                break

            except asyncio.TimeoutError:
                await ctx.send("⏰ Time's up! Cancelled.")
                return

        logging.info(
            f"{ctx.author} wants each password to be {manychar} characters long"
        )

        characters = (
            "!@#$%&*_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )

        await ctx.send(
            f"✅ Generating {manypass} password(s) with {manychar} characters each... Check your DMs!"
        )

        passwords = []
        for _ in range(manypass):
            password = "".join(random.choice(characters) for _ in range(manychar))
            passwords.append(password)

        try:
            if manypass == 1:
                await ctx.author.send(f"🔑 **Your Password:** `{passwords[0]}`")
            else:
                msg = "🔑 **Your Passwords:**\n"
                for i, pwd in enumerate(passwords, 1):
                    msg += f"**{i}.** `{pwd}`\n"
                await ctx.author.send(msg)

            await ctx.author.send("⚠️ Save these somewhere safe! I don't store them.")
            logging.info(f"{ctx.author} successfully generated {manypass} passwords")

        except:
            await ctx.reply("❌ I couldn't DM you! Check your privacy settings.")
            logging.error(f"Couldn't DM {ctx.author} for password generation")
