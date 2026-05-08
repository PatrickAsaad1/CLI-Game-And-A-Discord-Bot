# games/cafe.py
import asyncio
from Utils.Logger import setup_logging
from datetime import datetime
from Utils.Helpers import return_to_menu, returnx

logging = setup_logging()


def setup(bot):
    @bot.command(name="cafe", aliases=["Cafe", "CAFE"])
    async def cafe(ctx):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        """Cafe ordering system."""
        logging.info(f"{ctx.author} selected cafe system")
        max_quantities = {
            "pizza": 10,
            "burger": 15,
            "tea": 50,
            "coffee": 50,
            "latte": 50,
        }
        DEFAULT_MAX_QTY = 50
        menu_prices = {"pizza": 8, "burger": 7, "tea": 2, "coffee": 3, "latte": 4}
        menu_items = ", ".join(menu_prices.keys())

        await ctx.reply("Welcome to Pat Cafe!")

        orders = []
        total_price = 0

        while True:
            try:
                await ctx.send(
                    f"{ctx.author.mention}, what do you want today? Here's what we are serving:\n{menu_items}"
                )
                order_msg = await bot.wait_for("message", timeout=30.0, check=check)

                if returnx(order_msg.content):
                    return

                order = order_msg.content.lower().strip()

                if order not in menu_prices:
                    await ctx.reply(
                        f"Sorry, we don't have '{order}' on the menu. Try again."
                    )
                    logging.warning(f"{ctx.author} requested invalid item: {order}")
                    continue

                max_qty = max_quantities.get(order, DEFAULT_MAX_QTY)
                if order == "pizza":
                    await ctx.reply("🍕 Great choice! Pizza is delicious!")
                elif order == "burger":
                    await ctx.reply("🍔 Yummy! Burgers are always a good idea!")
                else:
                    await ctx.reply(f"☕ {order.title()} is a perfect pick-me-up!")

            except asyncio.TimeoutError:
                await ctx.send("⏰ Time's up! Order cancelled.")
                return

            while True:
                try:
                    await ctx.send(f"How many {order} would you like?")
                    qty_msg = await bot.wait_for("message", timeout=30.0, check=check)

                    if returnx(qty_msg.content):
                        return

                    qty_input = qty_msg.content.strip()

                    if not qty_input.isdigit():
                        await ctx.reply("Please enter a valid number!")
                        logging.warning("User put a non-number input")
                        continue

                    qty = int(qty_input)
                    if qty <= 0:
                        logging.warning("User put a negative number")
                        await ctx.reply("Please enter a positive number!")
                    elif qty > max_qty:
                        await ctx.reply(
                            f"Sorry, we can only serve up to {max_qty} {order}s at a time."
                        )
                        logging.warning(
                            f"User wanted to order {qty} {order} (max {max_qty})"
                        )
                    else:
                        break

                except asyncio.TimeoutError:
                    await ctx.send("⏰ Time's up! Order cancelled.")
                    return

            orders.append({"item": order, "quantity": qty, "price": menu_prices[order]})
            total_price += qty * menu_prices[order]

            if qty > 1:
                if order.endswith("y"):
                    item_word = order[:-1] + "ies"
                elif order in ["tea", "coffee", "latte"]:
                    item_word = order
                else:
                    item_word = order + "s"
            else:
                item_word = order

            await ctx.reply(f"✓ Added {qty} {item_word} to your order.")
            logging.info(
                f"Added {qty} x {order} to order. Current total: ${total_price:.2f}"
            )

            try:
                await ctx.reply("Would you like to order something else? (y/n):")
                more_msg = await bot.wait_for("message", timeout=30.0, check=check)

                if returnx(more_msg.content):
                    return

                more = more_msg.content.lower().strip()
                if more not in ["y", "yes"]:
                    break
            except asyncio.TimeoutError:
                await ctx.send("⏰ Time's up! Finishing your order.")
                break

        if orders:
            summary_lines = ["\n" + "=" * 40, "     Your Order Summary", "=" * 40]
            for item in orders:
                summary_lines.append(
                    f"• {item['quantity']} x {item['item']}: ${item['quantity'] * item['price']:.2f}"
                )
            summary_lines.extend(
                [
                    "-" * 40,
                    f"Total: ${total_price:.2f}",
                    "=" * 40,
                    "Thank you for visiting Pat Cafe! ☕",
                ]
            )
            await ctx.send("\n".join(summary_lines))
            logging.info(f"{ctx.author} completed order. Total: ${total_price:.2f}")
        else:
            await ctx.send("No items ordered. Come back soon!")
