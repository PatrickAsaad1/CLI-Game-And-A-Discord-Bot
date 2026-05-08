# Bot/Utilities/SetChannel.py
import discord
from discord.ext import commands
from Utils.Config import (
    add_allowed_channel,
    remove_allowed_channel,
    get_allowed_channels,
    set_lyrics_channel,
    remove_lyrics_channel,
    set_rap_news_channel,
    set_pet_channel,
    set_game_news_channel,
    remove_rap_news_channel,
    remove_game_news_channel,
)
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="setchannel", aliases=["SetChannel", "SETCHANNEL"])
    @commands.has_permissions(administrator=True)
    async def set_channel(ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        add_allowed_channel(ctx.guild.id, channel.id)
        await ctx.reply(f"✅ {channel.mention} added to allowed channels!")
        logging.info(f"{ctx.author} added {channel.name} in {ctx.guild.name}")

    @bot.command(name="removechannel", aliases=["RemoveChannel", "REMOVECHANNEL"])
    @commands.has_permissions(administrator=True)
    async def remove_channel(ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        remove_allowed_channel(ctx.guild.id, channel.id)
        await ctx.reply(f"🗑️ {channel.mention} removed from allowed channels!")
        logging.info(f"{ctx.author} removed {channel.name} in {ctx.guild.name}")

    @bot.command(name="channels", aliases=["Channels", "CHANNELS"])
    @commands.has_permissions(administrator=True)
    async def list_channels(ctx):
        channels = get_allowed_channels(ctx.guild.id)
        if not channels:
            await ctx.reply("No channels set! Use `!setchannel #channel` to add one.")
            return
        mentions = []
        for cid in channels:
            channel = ctx.guild.get_channel(cid)
            if channel:
                mentions.append(channel.mention)
        await ctx.reply(f"📋 Allowed channels: {', '.join(mentions)}")

    @bot.command(name="setlyrics", aliases=["SetLyrics", "SETLYRICS"])
    @commands.has_permissions(administrator=True)
    async def set_lyrics(ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        set_lyrics_channel(ctx.guild.id, channel.id)
        await ctx.reply(f"✅ Lyrics will be sent to {channel.mention}!")
        logging.info(
            f"{ctx.author} set lyrics channel to {channel.name} in {ctx.guild.name}"
        )

    @bot.command(name="removelyrics", aliases=["RemoveLyrics", "REMOVELYRICS"])
    @commands.has_permissions(administrator=True)
    async def remove_lyrics(ctx):
        remove_lyrics_channel(ctx.guild.id)
        await ctx.reply("🗑️ Lyrics channel removed!")
        logging.info(f"{ctx.author} removed lyrics channel in {ctx.guild.name}")

    @bot.command(name="setrapnews", aliases=["SetRapNews", "SETRAPNEWS"])
    @commands.has_permissions(administrator=True)
    async def set_rap_news(ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        set_rap_news_channel(ctx.guild.id, channel.id)
        await ctx.reply(f"✅ Rap news will be sent to {channel.mention}!")
        logging.info(
            f"{ctx.author} set rap news channel to {channel.name} in {ctx.guild.name}"
        )

    @bot.command(name="sethourlypets", aliases=["SetHourlyPets", "SETHOURLYPETS"])
    @commands.has_permissions(administrator=True)
    async def set_hourly_pets(ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        set_pet_channel(ctx.guild.id, channel.id)
        await ctx.reply(f"✅ Hourly pet pictures will be sent to {channel.mention}!")
        logging.info(
            f"{ctx.author} set pet channel to {channel.name} in {ctx.guild.name}"
        )

    @bot.command(name="setgamenews", aliases=["SetGameNews", "SETGAMENEWS"])
    @commands.has_permissions(administrator=True)
    async def set_game_news(ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        set_game_news_channel(ctx.guild.id, channel.id)
        await ctx.trply(f"✅ Gaming news will be sent to {channel.mention}!")
        logging.info(
            f"{ctx.author} set game news channel to {channel.name} in {ctx.guild.name}"
        )
    @bot.command(name="removerapnews", aliases=["RemoveRapNews", "REMOVERAPNEWS"])
    @commands.has_permissions(administrator=True)
    async def remove_rap_news(ctx):
        remove_rap_news_channel(ctx.guild.id)
        await ctx.trply("🗑️ Rap news channel removed!")
        logging.info(f"{ctx.author} removed rap news channel in {ctx.guild.name}")

    @bot.command(name="removegamenews", aliases=["RemoveGameNews", "REMOVEGAMENEWS"])
    @commands.has_permissions(administrator=True)
    async def remove_game_news(ctx):
        remove_game_news_channel(ctx.guild.id)
        await ctx.reply("🗑️ Gaming news channel removed!")
        logging.info(f"{ctx.author} removed game news channel in {ctx.guild.name}")
