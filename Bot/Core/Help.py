# Bot/Core/Help.py
import discord
from discord.ext import commands
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):

    bot.remove_command("help")

    @bot.command(
        name="help", aliases=["Help", "HELP", "h", "H", "commands", "Commands"]
    )
    async def custom_help(ctx, command_name: str = None):
        logging.info(f"Help command used by: {ctx.author}")

        if command_name:
            await send_command_help(ctx, command_name)
            return

        embed = discord.Embed(
            title="📚 **Help Menu**",
            description="Use `!help <command>` for more details on a specific command.",
            color=discord.Color.blue(),
        )

        games = (
            "`!rps` - Rock Paper Scissors (solo or versus a friend)\n"
            "`!guess` - Guess the number game (reach 3 points to win)\n"
            "`!number` - Guess a number between 1-20 (5 attempts)\n"
        )
        embed.add_field(name="🎮 **Games**", value=games, inline=False)

        sim = "`!cafe` - Pat Cafe ordering system\n"
        embed.add_field(name="🏪 **Simulation**", value=sim, inline=False)

        fun = (
            "`!quote` - Get a random inspirational quote\n"
            "`!picker` - Create a list and pick random items\n"
            "`!cat` - Get a random cat picture\n"
            "`!dog` - Get a random dog picture\n"
            "`!coinflip` - Flip a coin (heads or tails)\n"
            "`!roll` - Roll a dice (default 6-sided)\n"
            "`!joke` - Get a random dad joke\n"
            "`!meme` - Get a random meme\n"
            "`!advice` - Get a random piece of advice\n"
            "`!lyrics <Artist - Song>` - Get song lyrics\n"
            "`!ask <question>` - Ask AI a question\n"
        )
        embed.add_field(name="🎉 **Fun**", value=fun, inline=False)

        utils = (
            "`!ping` - Check the bot's connection latency\n"
            "`!calc <expression>` - Perform arithmetic calculations\n"
            "`!weather <city>` - Get current weather for any city\n"
            "`!serverinfo` - Display server information\n"
            "`!qr <text>` - Generate a QR code\n"
            "`!morse <text>` - Convert text to Morse code\n"
            "`!remind <time> <message>` - Set a reminder (e.g., `!remind 5m break`)\n"
            "`!say <message>` - The bot will DM you the message\n"
            "`!repeat <message>` - Spam a message to your DMs (max 10)\n"
            "`!reply <message>` - The bot will reply to your message\n"
            "`!search` - Search for a word in a large text block\n"
        )
        embed.add_field(name="🔧 **Utilities**", value=utils, inline=False)

        admin = (
            "`!setchannel <#channel>` / `!removechannel <#channel>` - Manage command channels\n"
            "`!channels` - List allowed channels\n"
            "`!setlyrics <#channel>` / `!removelyrics` - Set/Remove lyrics channel\n"
            "`!setrapnews <#channel>` / `!removerapnews` - Set/Remove rap news channel\n"
            "`!setgamenews <#channel>` / `!removegamenews` - Set/Remove gaming news channel\n"
            "`!sethourlypets <#channel>` - Set hourly pet pictures channel\n"
        )
        embed.add_field(name="⚙️ **Admin**", value=admin, inline=False)

        security = (
            "`!passgen` - Generate secure random passwords\n"
            "`!encrypt <message>` - Encrypt a message and get the key\n"
            "`!decrypt` - Decrypt a message using the key\n"
        )
        embed.add_field(name="🔐 **Security**", value=security, inline=False)

        help_text = (
            "`!help` - Display this message\n"
            "`!help <command>` - View detailed information about a command\n"
        )
        embed.add_field(name="📖 **Help**", value=help_text, inline=False)

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )

        await ctx.reply(embed=embed)


async def send_command_help(ctx, command_name):
    command_name = command_name.lower()

    if command_name == "ping":
        embed = discord.Embed(
            title="📖 `!ping`",
            description="Check the bot's connection latency to Discord.",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!ping`", inline=False)
        embed.add_field(name="Example", value="`!ping` → `🏓 Pong! 47ms`", inline=False)

    elif command_name == "calc":
        embed = discord.Embed(
            title="🧮 `!calc`",
            description="Perform basic arithmetic calculations with support for multiple operations.",
            color=discord.Color.green(),
        )
        embed.add_field(
            name="Usage",
            value="`!calc <expression>`\nSupports both spaced and unspaced formats.",
            inline=False,
        )
        embed.add_field(
            name="Operators",
            value="`+` (addition)\n`-` (subtraction)\n`*` or `x` (multiplication)\n`/` (division)",
            inline=False,
        )
        embed.add_field(
            name="Examples",
            value="`!calc 5 + 3` → `🧮 5.0 + 3.0 = 8.0`\n`!calc 5+3` → `🧮 5+3 = 8.0`\n`!calc 5 + 3 + 2` → `🧮 5 + 3 + 2 = 10.0`",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Calculations are performed left-to-right. Standard order of operations is not applied.",
            inline=False,
        )

    elif command_name == "rps":
        embed = discord.Embed(
            title="🪨📄✂️ `!rps`",
            description="Play Rock Paper Scissors against the computer or challenge a friend!",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!rps`", inline=False)
        embed.add_field(
            name="Solo Mode",
            value="Play against the computer. First to 3 points wins.\nType `rock`, `paper`, or `scissors` when prompted.\nType `quit` to stop.",
            inline=False,
        )
        embed.add_field(
            name="Multiplayer Mode",
            value="Type `yes` when asked if you want to play with a friend, then mention the user you wish to challenge.\nChoices are submitted privately via DM.\nOnly the final result is announced in the channel.",
            inline=False,
        )

    elif command_name == "guess":
        embed = discord.Embed(
            title="🎲 `!guess`",
            description="Guess the randomly generated number. Reach 3 points to win!",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!guess`", inline=False)
        embed.add_field(
            name="Difficulties",
            value="`easy` — Numbers 1-3\n`med` or `medium` — Numbers 1-5\n`hard` — Numbers 1-10",
            inline=False,
        )
        embed.add_field(
            name="How to Play",
            value="Select a difficulty level, then guess the number.\nCorrect guess: +1 point\nIncorrect guess: -1 point (if score > 0)\nType `quit` to exit the game.",
            inline=False,
        )

    elif command_name == "number":
        embed = discord.Embed(
            title="🔢 `!number`",
            description="Guess a number between 1 and 20. You have 5 attempts.",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!number`", inline=False)
        embed.add_field(
            name="How to Play",
            value="The bot will select a random number between 1 and 20.\nYou have 5 attempts to guess correctly.\nThe bot will tell you if your guess is too high or too low.\nType `quit` to exit the game.",
            inline=False,
        )

    elif command_name == "say":
        embed = discord.Embed(
            title="📨 `!say`",
            description="Have the bot send a private message to you containing your text.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Usage", value="`!say <message>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Say`, `!send`, `!Send`, `!dm`, `!Dm`, `!DM`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value='`!say Hello, world!` → The bot will DM you "Hello, world!"',
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="If your DMs are closed, the bot will be unable to send the message and will notify you in the channel.",
            inline=False,
        )

    elif command_name == "repeat":
        embed = discord.Embed(
            title="🔁 `!repeat`",
            description="Have the bot spam a message to your DMs.",
            color=discord.Color.purple(),
        )
        embed.add_field(name="Usage", value="`!repeat <message>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Repeat`, `!REPEAT`, `!spam`, `!Spam`, `!SPAM`",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="After typing the command, the bot will ask how many times you want the message sent (maximum 10).\nThe messages will be delivered to your DMs.",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!repeat Hello!` → Bot asks for amount → You type `5` → Bot DMs you 'Hello!' 5 times",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Maximum is 10 times to prevent spam. If your DMs are closed, the command will fail.",
            inline=False,
        )

    elif command_name == "reply":
        embed = discord.Embed(
            title="💬 `!reply`",
            description="The bot will reply directly to the message that triggered this command.",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="Usage", value="`!reply` or `!reply <message>`", inline=False
        )
        embed.add_field(name="Aliases", value="`!Reply`, `!REPLY`, `!r`", inline=False)
        embed.add_field(
            name="Example",
            value="`!reply Hello!` → The bot replies to your message with 'Hello!'",
            inline=False,
        )

    elif command_name == "quote":
        embed = discord.Embed(
            title="💬 `!quote`",
            description="Get a random inspirational quote from the ZenQuotes API.",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Usage", value="`!quote`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Quotes`, `!QUOTES`, `!QUOTE`, `!Quote`, `!q`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!quote` → `✨ When your intuition is strong, follow it. — *Lolly Daskal*`",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Quotes are fetched from ZenQuotes API. Requires internet connection.",
            inline=False,
        )

    elif command_name in ["passgen", "password", "genpass", "bgen"]:
        embed = discord.Embed(
            title="🔑 `!passgen`",
            description="Generate secure random passwords.",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!passgen`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!password`, `!genpass`, `!bgen`",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="The bot will ask how many passwords you want (max 10) and how many characters per password (4-50).\nPasswords include letters, numbers, and symbols.",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!passgen` → Bot asks for amount → You type `3` → Bot asks for length → You type `16` → Bot DMs you 3 passwords of 16 characters each",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Passwords are sent via DM for privacy. Type `quit` to cancel at any time.",
            inline=False,
        )

    elif command_name == "search":
        embed = discord.Embed(
            title="🔍 `!search`",
            description="Search for a word in a large block of text.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Usage", value="`!search`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!SEARCH`, `!Search`, `!searchtxt`",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="Paste a large block of text, then enter the word you want to find.\nThe bot will tell you if the word exists in the text.",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Maximum text length is 50,000 characters. Type `quit` to cancel.",
            inline=False,
        )

    elif command_name in ["encrypt", "enc"]:
        embed = discord.Embed(
            title="🔒 `!encrypt`",
            description="Encrypt a message using Fernet encryption.",
            color=discord.Color.dark_blue(),
        )
        embed.add_field(name="Usage", value="`!encrypt <message>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Encrypt`, `!ENCRYPT`, `!enc`",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="The bot generates a unique key and encrypts your message.\nBoth the encrypted message and key are sent to your DMs.",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!encrypt Hello World` → Bot DMs you the encrypted message and key",
            inline=False,
        )
        embed.add_field(
            name="⚠️ Important",
            value="**SAVE THE KEY!** Without it, the message cannot be decrypted. The bot does not store keys.",
            inline=False,
        )

    elif command_name in ["decrypt", "dec"]:
        embed = discord.Embed(
            title="🔓 `!decrypt`",
            description="Decrypt a message using the provided key.",
            color=discord.Color.dark_blue(),
        )
        embed.add_field(name="Usage", value="`!decrypt`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Decrypt`, `!DECRYPT`, `!dec`",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="The bot will DM you and ask for the encrypted message, then the key.\nIf both are correct, the decrypted message is sent to your DMs.",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="For privacy, the entire process happens in DMs. The bot never sees your decrypted message in the channel.",
            inline=False,
        )

    elif command_name in ["picker", "wheel"]:
        embed = discord.Embed(
            title="🎲 `!picker`",
            description="Create a custom list and let the bot pick random items from it.",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Usage", value="`!picker`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Picker`, `!PICKER`, `!Wheel`",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="1. Add items to your list one by one\n2. Type `done` when finished\n3. Optionally remove items by number\n4. The bot picks random items from your list",
            inline=False,
        )
        embed.add_field(
            name="Commands During Pick",
            value="`done` - Finish adding items\n`quit` - Exit at any time\n`y/n` - Pick again or stop",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!picker` → Add 'Pizza', 'Burger', 'Sushi' → `done` → Bot picks: 'Sushi'",
            inline=False,
        )

    elif command_name in ["cafe", "Cafe", "CAFE"]:
        embed = discord.Embed(
            title="🏪 `!cafe`",
            description="Pat Cafe ordering system - order food and drinks!",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!cafe`", inline=False)
        embed.add_field(name="Aliases", value="`!Cafe`, `!CAFE`", inline=False)
        embed.add_field(
            name="Menu",
            value="🍕 Pizza - $8\n🍔 Burger - $7\n☕ Tea - $2\n☕ Coffee - $3\n☕ Latte - $4",
            inline=False,
        )
        embed.add_field(
            name="How it Works",
            value="1. Choose an item from the menu\n2. Enter quantity (limits apply)\n3. Add more items or finish\n4. Get your total bill",
            inline=False,
        )
        embed.add_field(
            name="Quantity Limits",
            value="Pizza: 10 | Burger: 15 | Drinks: 50",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Type `quit` at any time to cancel your order.",
            inline=False,
        )

    elif command_name in ["remind", "reminder"]:
        embed = discord.Embed(
            title="⏰ `!remind`",
            description="Set a reminder and the bot will DM you when time is up.",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Usage", value="`!remind <time> <message>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Remind`, `!REMIND`, `!reminder`",
            inline=False,
        )
        embed.add_field(
            name="Time Formats",
            value="`30s` - 30 seconds\n`5m` - 5 minutes\n`2h` - 2 hours",
            inline=False,
        )
        embed.add_field(
            name="Examples",
            value="`!remind 30s check food`\n`!remind 5m meeting`\n`!remind 2h take a break`",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Maximum reminder is 2 hours. Reminders are lost if the bot restarts.",
            inline=False,
        )

    elif command_name == "weather":
        embed = discord.Embed(
            title="🌤️ `!weather`",
            description="Get current weather for any city in the world.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Usage", value="`!weather <city>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Weather`, `!WEATHER`, `!temp`",
            inline=False,
        )
        embed.add_field(
            name="Examples",
            value='`!weather Cairo`\n`!weather London`\n`!weather "New York"`',
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Uses Open-Meteo API. Works for virtually any city worldwide.",
            inline=False,
        )

    elif command_name in ["cat", "kitty", "meow"]:
        embed = discord.Embed(
            title="🐱 `!cat`",
            description="Get a random cat picture!",
            color=discord.Color.pink(),
        )
        embed.add_field(name="Usage", value="`!cat`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Cat`, `!CAT`, `!kitty`, `!meow`",
            inline=False,
        )

    elif command_name in ["dog", "Dog", "DOG"]:
        embed = discord.Embed(
            title="🐶 `!dog`",
            description="Get a random dog picture!",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Usage", value="`!dog`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Dog`, `!DOG`",
            inline=False,
        )

    elif command_name in ["coinflip", "cf", "flip", "coin"]:
        embed = discord.Embed(
            title="🪙 `!coinflip`",
            description="Flip a coin and get heads or tails!",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Usage", value="`!coinflip`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Coinflip`, `!COINFLIP`, `!cf`, `!flip`, `!coin`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!coinflip` → 🪙 The coin landed on **Heads**!",
            inline=False,
        )

    elif command_name in ["roll", "dice"]:
        embed = discord.Embed(
            title="🎲 `!roll`",
            description="Roll a dice and get a random number!",
            color=discord.Color.green(),
        )
        embed.add_field(name="Usage", value="`!roll`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Roll`, `!ROLL`, `!dice`, `!Dice`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!roll` → 🎲 You rolled a **4**!",
            inline=False,
        )

    elif command_name in ["joke", "dadjoke"]:
        embed = discord.Embed(
            title="😂 `!joke`",
            description="Get a random dad joke!",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Usage", value="`!joke`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Joke`, `!JOKE`, `!DADJOKE`, `!dadjoke`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!joke` → 😂 Why don't scientists trust atoms? Because they make up everything!",
            inline=False,
        )

    elif command_name in ["meme", "memes"]:
        embed = discord.Embed(
            title="😂 `!meme`",
            description="Get a random meme from Reddit!",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Usage", value="`!meme`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Meme`, `!MEME`, `!memes`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!meme` → Sends a random meme image",
            inline=False,
        )

    elif command_name in ["serverinfo", "si"]:
        embed = discord.Embed(
            title="📊 `!serverinfo`",
            description="Display detailed information about the current server.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Usage", value="`!serverinfo`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!ServerInfo`, `!SERVERINFO`, `!si`",
            inline=False,
        )
        embed.add_field(
            name="Shows",
            value="Server name, owner, member count, creation date, channels, and roles",
            inline=False,
        )

    elif command_name in ["qr", "qrcode"]:
        embed = discord.Embed(
            title="🔲 `!qr`",
            description="Generate a QR code from text or a URL.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Usage", value="`!qr <text or URL>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!QR`, `!Qr`, `!qrcode`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!qr https://github.com` → Sends a QR code image",
            inline=False,
        )

    elif command_name == "morse":
        embed = discord.Embed(
            title="📡 `!morse`",
            description="Convert text to Morse code.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Usage", value="`!morse <text>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Morse`, `!MORSE`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!morse hello` → .... . .-.. .-.. ---",
            inline=False,
        )

    elif command_name in ["ask", "ai"]:
        embed = discord.Embed(
            title="🤖 `!ask`",
            description="Ask the AI a question and get a response.",
            color=discord.Color.purple(),
        )
        embed.add_field(name="Usage", value="`!ask <question>`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Ask`, `!ASK`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!ask What is Python?`",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Uses Pollinations AI API. Responses may vary in quality.",
            inline=False,
        )

    elif command_name in ["advice"]:
        embed = discord.Embed(
            title="💡 `!advice`",
            description="Get a random piece of advice.",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Usage", value="`!advice`", inline=False)
        embed.add_field(
            name="Aliases",
            value="`!Advice`, `!ADVICE`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!advice` → 💡 Never regret anything that made you smile.",
            inline=False,
        )

    elif command_name in ["lyrics", "lyric"]:
        embed = discord.Embed(
            title="🎵 `!lyrics`",
            description="Get the lyrics of any song.",
            color=discord.Color.purple(),
        )
        embed.add_field(
            name="Usage", value="`!lyrics <Artist> - <Song Name>`", inline=False
        )
        embed.add_field(
            name="Aliases",
            value="`!Lyrics`, `!LYRICS`, `!Lyric`, `!LYRIC`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`!lyrics Coldplay - Yellow`",
            inline=False,
        )
        embed.add_field(
            name="Note",
            value="Uses lyrics.ovh API. Use `Artist - Song` format.",
            inline=False,
        )

    elif command_name in ["setchannel", "removechannel", "channels"]:
        embed = discord.Embed(
            title="⚙️ Channel Management",
            description="Admin commands to control where the bot works.",
            color=discord.Color.purple(),
        )
        embed.add_field(
            name="`!setchannel <#channel>` / `!removechannel <#channel>`",
            value="Add or remove a channel where commands can be used.",
            inline=False,
        )
        embed.add_field(
            name="`!channels`",
            value="List all allowed channels for this server.",
            inline=False,
        )
        embed.add_field(
            name="`!setlyrics <#channel>` / `!removelyrics`",
            value="Set or remove the lyrics command channel.",
            inline=False,
        )
        embed.add_field(
            name="`!setrapnews <#channel>` / `!removerapnews`",
            value="Set or remove the AI rap news channel.",
            inline=False,
        )
        embed.add_field(
            name="`!setgamenews <#channel>` / `!removegamenews`",
            value="Set or remove the gaming news channel.",
            inline=False,
        )
        embed.add_field(
            name="`!sethourlypets <#channel>`",
            value="Set the channel for hourly cat/dog pictures.",
            inline=False,
        )
        embed.add_field(
            name="Permission",
            value="Administrator only.",
            inline=False,
        )

    elif command_name == "help":
        embed = discord.Embed(
            title="📚 `!help`",
            description="You are currently viewing it!",
            color=discord.Color.green(),
        )
        embed.add_field(
            name="Usage",
            value="`!help` — Display all available commands\n`!help <command>` — View detailed information about a specific command",
            inline=False,
        )

    else:
        embed = discord.Embed(
            title="❌ Command Not Found",
            description=f"No help information is available for `{command_name}`.",
            color=discord.Color.red(),
        )
        embed.add_field(
            name="Tip",
            value="Use `!help` to see a list of all available commands.",
            inline=False,
        )

    embed.set_footer(
        text=f"Requested by {ctx.author.name}",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
    )
    await ctx.reply(embed=embed)
