import Utils.Windows_Fix
import os
import discord
import asyncio
import logging
from discord.ext import commands
from dotenv import load_dotenv
from Utils.Logger import setup_logging
from Utils.Config import get_allowed_channels
from Bot.Core import Ping, Help, Admin
from Bot.Games import Rps, Guess_The_Num, Number_Game
from Bot.Fun import (
    Quotes,
    Random_Picker,
    Weather,
    Cat_Dog,
    CoinFlip,
    Roll,
    Joke,
    Meme,
    HourlyPets,
    Advice,
    Lyrics,
    RapNews,
    GameNews,
    MCTiers,
)
from Bot.Utilities import (
    Calculator,
    Bot_Talk,
    TextSearch,
    Reminder,
    Cafe,
    SetChannel,
    ServerInfo,
    QR,
    Morse,
    Groq,
)
from Bot.Security import Password, EncryptDecrypt

setup_logging()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


@bot.check
async def check_all(ctx):
    """Block DMs and restrict commands to set channels."""
    if ctx.guild is None:
        await ctx.send("❌ Commands cannot be used in DMs!")
        return False

    allowed_channels = get_allowed_channels(ctx.guild.id)
    if allowed_channels and ctx.channel.id not in allowed_channels:
        await ctx.send("❌ You cannot use commands here!")
        return False

    return True


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        logging.info(f"{ctx.author} tried to use command in wrong channel")
        return
    elif isinstance(error, commands.CommandNotFound):
        logging.info(f"{ctx.author} tried unknown command: {ctx.message.content}")
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        return
    else:
        logging.error(f"Unexpected error: {error}")
        raise error


@bot.event
async def on_member_join(member):
    try:
        await member.send(
            f"Welcome {member.mention}, Welcome to ✧ Meta Competition ✧!\n"
            f"Please make sure to check <#1454850144943083562> and <#1454885928983204056>\n"
            f"Have Fun!"
        )
    except:
        pass


@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    logging.info(f"{bot.user} has connected to Discord!")
    await bot.change_presence(activity=discord.Game(name="Made with Python 🐍"))
    HourlyPets.send_pet_pic.bot = bot
    HourlyPets.send_pet_pic.start()
    RapNews.send_rap_news.bot = bot
    RapNews.send_rap_news.start()
    GameNews.send_game_news.bot = bot
    GameNews.send_game_news.start()
    for guild in bot.guilds:
        channel_ids = get_allowed_channels(guild.id)
        if channel_ids:
            for channel_id in channel_ids:  # ← Loop through all channels
                channel = guild.get_channel(channel_id)
                if channel:
                    try:
                        await channel.send(f"{bot.user} Is Ready To Go")
                    except:
                        continue
        else:
            # No channels set - find first available
            for channel in guild.text_channels:
                permissions = channel.permissions_for(guild.me)
                if permissions.send_messages:
                    try:
                        await channel.send(
                            f"{bot.user} Is Ready To Go\n💡 Use `!setchannel #channel` to set a specific channel!"
                        )
                        break
                    except:
                        continue


# Core
Ping.setup(bot)
Help.setup(bot)
Admin.setup(bot)

# Games
Rps.setup(bot)
Guess_The_Num.setup(bot)
Number_Game.setup(bot)

# Fun
Quotes.setup(bot)
Random_Picker.setup(bot)
Weather.setup(bot)
Cat_Dog.setup(bot)
CoinFlip.setup(bot)
Roll.setup(bot)
Joke.setup(bot)
Meme.setup(bot)
Lyrics.setup(bot)
# RapNews.setup(bot)
# GameNews.setup(bot) We don't need them they are already at on_ready, so they will work without setup(bot)
Advice.setup(bot)
MCTiers.setup(bot)

# Utilities
Calculator.setup(bot)
Bot_Talk.setup(bot)
TextSearch.setup(bot)
Reminder.setup(bot)
Cafe.setup(bot)
SetChannel.setup(bot)
ServerInfo.setup(bot)
QR.setup(bot)
Morse.setup(bot)
Groq.setup(bot)

# Security
Password.setup(bot)
EncryptDecrypt.setup(bot)

bot.run(TOKEN)
