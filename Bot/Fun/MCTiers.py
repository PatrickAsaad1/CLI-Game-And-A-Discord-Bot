# Bot/Fun/MCTiers.py
from Utils.Logger import setup_logging
import requests
from requests.exceptions import Timeout as RequestsTimeout
import discord
import asyncio
import urllib.parse

logging = setup_logging()


def truncate_field(value, max_len=1024):
    """Trim a string to max_len characters for Discord embed fields."""
    if len(value) <= max_len:
        return value
    return value[: max_len - 15] + "… (truncated)"


def fetch_mc_profile(username):
    """Synchronous HTTP call for MCTiers API."""
    encoded = urllib.parse.quote_plus(username)
    return requests.get(
        f"https://mctiers.com/api/v2/profile/by-name/{encoded}", timeout=10
    )


def setup(bot):
    @bot.command(name="mc", aliases=["Mc", "MC", "mcinfo", "Mcinfo", "MCINFO"])
    async def mc(ctx, *, username: str = None):
        """Get Minecraft player info from MCTiers."""
        if not username:
            await ctx.send("❌ Please provide a username! Example: `!mc uku3lig`")
            return

        logging.info(f"{ctx.author} used !mc command for: {username}")

        try:
            response = await asyncio.to_thread(fetch_mc_profile, username)

            if response.status_code == 404:
                await ctx.send(f"❌ Player **{username}** not found!")
                return

            if response.status_code != 200:
                await ctx.send("❌ API error. Try again later!")
                return

            data = response.json()

            embed = discord.Embed(
                title=f"📊 {data['name']}",
                description=f"**UUID:** `{data['uuid']}`",
                color=discord.Color.green(),
            )

            embed.add_field(
                name="🌍 Region", value=data.get("region", "Unknown"), inline=True
            )
            embed.add_field(
                name="⭐ Points", value=str(data.get("points", 0)), inline=True
            )
            embed.add_field(
                name="🏆 Overall Rank",
                value=f"#{data.get('overall', 'N/A')}",
                inline=True,
            )

            if data.get("discord_id"):
                embed.add_field(
                    name="💬 Discord", value=f"<@{data['discord_id']}>", inline=True
                )

            rankings = data.get("rankings", {})
            if rankings:
                rankings_text = ""
                for mode, stats in rankings.items():
                    status = "🔴 Retired" if stats.get("retired") else "🟢 Active"
                    rankings_text += (
                        f"**{mode.replace('_', ' ').title()}**\n"
                        f"Tier {stats['tier']} • Pos {stats['pos']} • {status}\n"
                    )
                embed.add_field(
                    name="🎮 Gamemodes",
                    value=truncate_field(rankings_text),
                    inline=False,
                )

            if data.get("badges"):
                badges_text = "\n".join(
                    [f"🏅 {b['title']} — {b['desc']}" for b in data["badges"]]
                )
                embed.add_field(
                    name="🏅 Badges", value=truncate_field(badges_text), inline=False
                )

            embed.set_footer(text="Data from MCTiers API")
            await ctx.send(embed=embed)
            logging.info(f"MC info sent for {data['name']}")

        except RequestsTimeout:
            await ctx.send("❌ Request timed out. Try again later!")
            logging.error("MCTiers API timeout")
        except Exception as e:
            await ctx.send("❌ Could not fetch Minecraft info. Try again later!")
            logging.error(f"MCTiers API error: {e}")
