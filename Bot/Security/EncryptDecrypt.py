# Bot/Security/EncryptDecrypt.py
from Utils.Logger import setup_logging
import asyncio
import discord

try:
    from cryptography.fernet import Fernet, InvalidToken  # ← ADD InvalidToken

    FERNET_AVAILABLE = True
except ImportError:
    FERNET_AVAILABLE = False
    print("⚠️ cryptography not installed. Encrypt/Decrypt features disabled.")
    print("Run: pip install cryptography")

logging = setup_logging()


def setup(bot):
    @bot.command(name="encrypt", aliases=["Encrypt", "ENCRYPT", "enc"])
    async def encrypt(ctx, *, msg: str = None):
        """Encrypt a message using Fernet."""
        logging.info(f"{ctx.author} selected encrypt")

        if not FERNET_AVAILABLE:
            await ctx.send(
                "❌ This feature is currently unavailable. Please contact the bot owner."
            )
            return

        if not msg:
            await ctx.send("❌ Usage: `!encrypt <message>`")
            return

        try:
            key = Fernet.generate_key()
            cipher = Fernet(key)
            encrypted = cipher.encrypt(msg.encode())

            try:
                await ctx.author.send(
                    f"🔒 **Encrypted:** `{encrypted.decode()}`\n"
                    f"🔑 **Key (SAVE THIS):** `{key.decode()}`\n"
                    "⚠️ Without this key, the message is lost forever!"
                )
                await ctx.send("✅ Check your DMs for the encrypted message and key!")
                logging.info(f"{ctx.author} encrypted a message successfully")
            except:
                await ctx.send("❌ I couldn't DM you! Check your privacy settings.")
                logging.error(f"Couldn't DM {ctx.author} for encryption")

        except Exception as e:
            await ctx.send("❌ Encryption failed!")
            logging.error(f"Encryption error: {e}")

    @bot.command(name="decrypt", aliases=["Decrypt", "DECRYPT", "dec"])
    async def decrypt(ctx):
        """Decrypt a message using the key."""
        logging.info(f"{ctx.author} selected decrypt")

        if not FERNET_AVAILABLE:
            await ctx.send(
                "❌ This feature is currently unavailable. Please contact the bot owner."
            )
            return

        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

        try:
            await ctx.author.send("🔒 Please enter the **encrypted message**:")
            encrypted_msg = await bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.author.send("⏰ Time's up! Cancelled.")
            return

        try:
            await ctx.author.send("🔑 Please enter the **key**:")
            key_input = await bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.author.send("⏰ Time's up! Cancelled.")
            return

        try:
            key = key_input.content.encode()
            encrypted_bytes = encrypted_msg.content.encode()
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_bytes)

            await ctx.author.send(f"🔓 **Decrypted:** `{decrypted.decode()}`")
            await ctx.send("✅ Check your DMs for the decrypted message!")
            logging.info(f"{ctx.author} decrypted a message successfully")

        except InvalidToken:  # ← FIXED: Use imported InvalidToken
            await ctx.author.send(
                "❌ Invalid key or encrypted message!\n"
                "💡 Make sure you copied both EXACTLY as shown."
            )
            await ctx.send("❌ Decryption failed. Check your DMs.")
            logging.warning(f"{ctx.author} failed to decrypt - invalid key or message")
        except Exception as e:
            await ctx.author.send("❌ Decryption failed! Check your key and message.")
            await ctx.send("❌ Decryption failed. Check your DMs.")
            logging.warning(f"{ctx.author} failed to decrypt: {e}")
