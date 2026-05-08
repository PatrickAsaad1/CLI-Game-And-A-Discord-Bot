import asyncio
import re
from datetime import datetime
from Utils.Logger import setup_logging

logging = setup_logging()
reminder_tasks = {}  # task_id -> asyncio.Task


def setup(bot):
    @bot.command(name="remind", aliases=["Remind", "REMIND", "reminder"])
    async def remind(ctx, time: str = None, *, reminder: str = None):
        if not time or not reminder:
            await ctx.reply("❌ Usage: `!remind <time> <message>`")
            return

        # Parse time with better regex
        match = re.match(r"^(\d+)([smh])$", time.lower())
        if not match:
            await ctx.reply("❌ Invalid time format! Use `30s`, `5m`, or `2h`")
            return

        amount, unit = int(match.group(1)), match.group(2)
        time_dict = {"s": 1, "m": 60, "h": 3600}
        seconds = amount * time_dict[unit]

        if seconds <= 0 or seconds > 7200:
            await ctx.reply("❌ Time must be positive and ≤ 2 hours")
            return

        # Display time
        unit_names = {"s": "second", "m": "minute", "h": "hour"}
        display = f"{amount} {unit_names[unit]}{'s' if amount != 1 else ''}"

        await ctx.reply(f"⏰ Reminder set! I'll remind you in {display}.")

        # Store task for potential cancellation
        task = asyncio.create_task(_remind_user(ctx, seconds, reminder))
        reminder_tasks[ctx.author.id] = task

    async def _remind_user(ctx, seconds, reminder):
        try:
            await asyncio.sleep(seconds)
            await ctx.author.send(f"🔔 **Reminder:** {reminder}")
        except Exception:
            await ctx.send(f"{ctx.author.mention} 🔔 **Reminder:** {reminder}")
        finally:
            reminder_tasks.pop(ctx.author.id, None)

    @bot.command(name="cancel_remind")
    async def cancel_remind(ctx):
        if ctx.author.id in reminder_tasks:
            reminder_tasks[ctx.author.id].cancel()
            del reminder_tasks[ctx.author.id]
            await ctx.reply("✅ Reminder cancelled.")
        else:
            await ctx.reply("❌ No active reminder found.")
