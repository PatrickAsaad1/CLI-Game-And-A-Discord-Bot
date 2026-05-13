# Bot/Weather.py
import requests
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="weather", aliases=["Weather", "WEATHER", "temp", "Temp"])
    async def weather(ctx, *, city: str = None):
        """Get weather for any city in the world."""

        if not city:
            await ctx.reply(
                "❌ Please provide a city: `!weather Cairo` or `!weather London`"
            )
            return

        logging.info(f"{ctx.author} requested weather for: {city}")

        # Weather code to emoji
        weather_codes = {
            0: ("Clear", "☀️"),
            1: ("Mainly Clear", "🌤️"),
            2: ("Partly Cloudy", "⛅"),
            3: ("Overcast", "☁️"),
            45: ("Foggy", "🌫️"),
            48: ("Foggy", "🌫️"),
            51: ("Light Drizzle", "🌦️"),
            53: ("Drizzle", "🌦️"),
            55: ("Drizzle", "🌦️"),
            61: ("Light Rain", "🌧️"),
            63: ("Rain", "🌧️"),
            65: ("Heavy Rain", "🌧️"),
            71: ("Light Snow", "🌨️"),
            73: ("Snow", "❄️"),
            75: ("Heavy Snow", "❄️"),
            95: ("Thunderstorm", "⛈️"),
        }

        try:
            # Step 1: Geocode - Convert city name to coordinates
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            geo_response = requests.get(geo_url, timeout=10)
            geo_data = geo_response.json()

            if not geo_data.get("results"):
                await ctx.reply(f"❌ City '{city}' not found! Check spelling.")
                return

            location = geo_data["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]
            city_name = location["name"]
            country = location.get("country", "")
            admin1 = location.get("admin1", "")  # State/Region

            # Step 2: Get weather for those coordinates
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_response = requests.get(weather_url, timeout=10)
            weather_data = weather_response.json()

            current = weather_data["current_weather"]
            temp = current["temperature"]
            wind = current["windspeed"]
            code = current["weathercode"]

            desc, emoji = weather_codes.get(code, ("Unknown", "🌍"))

            # Build location string
            if admin1:
                location_str = f"{city_name}, {admin1}, {country}"
            else:
                location_str = f"{city_name}, {country}"

            msg = f"{emoji} **{location_str}**\n"
            msg += f"🌡️ **{temp}°C**\n"
            msg += f"📝 {desc}\n"
            msg += f"💨 Wind: {wind} km/h"

            logging.info(f"Weather sent for {location_str}: {temp}°C, {desc}")
            await ctx.reply(msg)

        except requests.exceptions.Timeout:
            await ctx.reply("❌ Request timed out. Try again later.")
            logging.error("Weather API timeout")
        except Exception as e:
            await ctx.reply("❌ Couldn't fetch weather. Try again later!")
            logging.error(f"Weather error: {e}")
