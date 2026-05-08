# Bot/Utilities/ServerInfo.py
import discord
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="serverinfo", aliases=["ServerInfo", "SERVERINFO", "si"])
    async def serverinfo(ctx):
        logging.info(f"{ctx.author} used !serverinfo")

        guild = ctx.guild

        embed = discord.Embed(title=f"📊 {guild.name}", color=discord.Color.blue())

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="👑 Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="🆔 Server ID", value=guild.id, inline=True)
        embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
        embed.add_field(
            name="📅 Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True
        )
        embed.add_field(name="💬 Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="🎭 Roles", value=len(guild.roles), inline=True)

        await ctx.reply(embed=embed)
