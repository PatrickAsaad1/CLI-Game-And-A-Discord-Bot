# Bot/Fun/Lyrics.py
import requests
from Utils.Logger import setup_logging
from Utils.Config import get_lyrics_channel

logging = setup_logging()


def setup(bot):
    @bot.command(name="lyrics", aliases=["Lyrics", "LYRICS", "lyric", "Lyric", "LYRIC"])
    async def lyric(ctx, *, query: str):
        logging.info(f"{ctx.author} used lyrics command")

        # Channel restriction
        lyrics_channel = get_lyrics_channel(ctx.guild.id)
        if lyrics_channel and ctx.channel.id != lyrics_channel:
            channel = ctx.guild.get_channel(lyrics_channel)
            if channel:
                await ctx.reply(f"❌ This command only works in {channel.mention}!")
            return

        if not query:
            await ctx.reply(
                "❌ Usage: `!lyrics Artist - Song Name`\nExample: `!lyrics Coldplay - Yellow`"
            )
            return

        if " - " not in query:
            await ctx.reply("❌ Please use format: `!lyrics Artist - Song Name`")
            return

        try:
            parts = query.split(" - ", 1)
            artist = parts[0].strip()
            song = parts[1].strip()

            apis = [
                f"https://api.lyrics.ovh/v1/{artist}/{song}",
                f"https://api.lyrics.ovh/v1/{artist.lower()}/{song.lower()}",
                f"https://api.lyrics.ovh/v1/{artist.title()}/{song.title()}",
                f"https://api.lyrics.ovh/v1/{artist.lower().replace(' ', '')}/{song.lower().replace(' ', '')}",
            ]

            lyrics = None
            for api_url in apis:
                response = requests.get(api_url)
                if response.status_code == 200:
                    json_data = response.json()
                    lyrics = json_data.get("lyrics", "No lyrics found.")
                    if lyrics and lyrics != "No lyrics found.":
                        break

            if not lyrics:
                await ctx.reply(f"❌ Lyrics not found for **{song}** by **{artist}**")
                return

            if len(lyrics) > 1900:
                await ctx.reply(f"🎵 **{song}** by **{artist}**\n")
                for i in range(0, len(lyrics), 1900):
                    chunk = lyrics[i : i + 1900]
                    await ctx.send(chunk)
            else:
                await ctx.reply(f"🎵 **{song}** by **{artist}**\n\n{lyrics}")

            logging.info(f"Lyrics shown for {song} by {artist}")

        except Exception as e:
            logging.error(f"Lyrics API error: {e}")
            await ctx.reply("❌ Could not fetch lyrics. Try again later!")
