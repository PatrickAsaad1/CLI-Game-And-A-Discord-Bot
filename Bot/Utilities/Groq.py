# Bot/Utilities/AI.py
import os
from groq import Groq
from dotenv import load_dotenv
from Utils.Logger import setup_logging

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

logging = setup_logging()

conversations = {}


def setup(bot):
    @bot.command(name="ask", aliases=["Ask", "ASK", "ai", "AI"])
    async def ask(ctx, *, msg: str = None):
        """Ask Groq AI a question."""
        if not msg:
            await ctx.reply("❌ Ask me something! Example: `!ask What is Python?`")
            return

        if not GROQ_API_KEY:
            await ctx.reply(
                "❌ This feature is currently unavailable. Please contact the bot owner."
            )
            logging.error("Groq API key not found")
            return

        user_id = ctx.author.id

        if user_id not in conversations:
            conversations[user_id] = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Keep answers concise.",
                }
            ]

        conversations[user_id].append({"role": "user", "content": msg})

        try:
            client = Groq(api_key=GROQ_API_KEY)

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=conversations[user_id],
                max_tokens=1000,
            )

            ai_reply = response.choices[0].message.content

            conversations[user_id].append({"role": "assistant", "content": ai_reply})

            if len(ai_reply) > 1900:
                ai_reply = ai_reply[:1900] + "..."

            await ctx.reply(ai_reply)
            logging.info(f"{ctx.author} used Groq: {msg[:50]}")

        except Exception as e:
            await ctx.reply("❌ Could not fetch AI response. Try again later!")
            logging.error(f"Groq error: {e}")

    @bot.command(name="forget", aliases=["Forget", "FORGET"])
    async def forget(ctx):
        """Clear your conversation history."""
        user_id = ctx.author.id
        if user_id in conversations:
            conversations[user_id] = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Keep answers concise.",
                }
            ]
        await ctx.reply("🧹 Conversation history cleared!")
        logging.info(f"{ctx.author} cleared their Groq conversation history")