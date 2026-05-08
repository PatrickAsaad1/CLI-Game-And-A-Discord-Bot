# Bot_games/Bot_Talk.py
from Utils.Logger import setup_logging
import discord
import asyncio

logging = setup_logging()


def setup(bot):

    @bot.command(name="say", aliases=["Say", "Send", "send", "SEND", "dm", "Dm", "DM"])
    async def say(ctx, *, msg: str):
        """Make the bot repeat what you say in DMs"""
        logging.info(f"User {ctx.author} used !say {msg}")
        try:
            await ctx.author.send(msg)
            await ctx.reply("✅ Check your DMs!")
            logging.info(f"{ctx.author} made the bot say {msg}")
        except:
            await ctx.reply("❌ I couldn't DM you! Check your privacy settings.")
            logging.error(f"Couldn't dm {ctx.author}")

    @bot.command(name="repeat", aliases=["Repeat", "REPEAT", "spam", "Spam", "SPAM"])
    async def repeat(ctx, *, msg: str):
        """Make the bot spam a message in your DMs"""
        logging.info(f"User {ctx.author} used !repeat {msg}")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.reply(
            "🔢 How many times do you want that message to be sent? (Max: 10)"
        )

        try:
            response = await bot.wait_for("message", timeout=30.0, check=check)
            times = int(response.content)

            if times <= 0:
                await ctx.send("❌ Number must be positive!")
                return

            if times > 10:
                await ctx.send("❌ Maximum is 10 times to prevent spam!")
                times = 10

            await ctx.send(f"✅ Sending `{msg}` {times} time(s) to your DMs!")

            for i in range(times):
                try:
                    await ctx.author.send(f"{i+1}. {msg}")
                    await asyncio.sleep(0.5)
                except:
                    await ctx.send("❌ I couldn't DM you! Check your privacy settings.")
                    logging.error(f"Couldn't dm {ctx.author} during repeat")
                    return

            await ctx.send("✅ Done! Check your DMs!")
            logging.info(f"{ctx.author} repeated message {times} times")

        except ValueError:
            await ctx.send("❌ Please enter a valid number!")
        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up! Command cancelled.")
        except Exception as e:
            await ctx.send("❌ Something went wrong!")
            logging.error(f"Repeat command error: {e}")

    @bot.command(name="reply", aliases=["Reply", "REPLY", "r"])
    async def reply_cmd(ctx, *, msg: str = None):
        """Reply to the message that triggered this command"""
        logging.info(f"User {ctx.author} used !reply")
        if msg:
            await ctx.reply(msg)
        else:
            await ctx.reply("This is a reply to your message!")
