# Bot_games/calculator.py (Upgraded)
from Utils.Logger import setup_logging

logging = setup_logging()


def setup(bot):
    @bot.command(name="calc", aliases=["Calc", "CALC", "calculate", "Calculate"])
    async def calc(ctx, *, expression: str = None):
        """Calculator: $calc 5+3 or $calc 5 + 3 + 2"""
        logging.info(f"Calc by {ctx.author}: {expression}")

        if not expression:
            await ctx.send("❌ Usage: `$calc 5 + 3` or `$calc 5+3`")
            return

        expression = expression.replace("x", "*").replace("×", "*").replace("÷", "/")

        if " " not in expression:
            for op in ["+", "-", "*", "/"]:
                if op in expression:
                    parts = expression.split(op)
                    if len(parts) == 2:
                        try:
                            num1 = float(parts[0])
                            num2 = float(parts[1])
                        except ValueError:
                            await ctx.reply("❌ Invalid numbers!")
                            return

                        if op == "+":
                            result = num1 + num2
                        elif op == "-":
                            result = num1 - num2
                        elif op == "*":
                            result = num1 * num2
                        elif op == "/":
                            if num2 == 0:
                                await ctx.reply("❌ Can't divide by zero!")
                                return
                            result = num1 / num2

                        await ctx.send(f"🧮 {expression} = {result}")
                        return
            await ctx.reply("❌ Invalid format! Use `$calc 5+3` or `$calc 5 + 3 + 2`")
            return

        parts = expression.split()

        if len(parts) < 3 or len(parts) % 2 == 0:
            await ctx.reply("❌ Invalid format! Example: `$calc 5 + 3 + 2`")
            return

        for i in range(1, len(parts), 2):
            if parts[i] not in ["+", "-", "*", "/"]:
                await ctx.reply(f"❌ Invalid operator: {parts[i]}")
                return

        try:
            result = float(parts[0])

            for i in range(1, len(parts), 2):
                op = parts[i]
                num = float(parts[i + 1])

                if op == "+":
                    result += num
                elif op == "-":
                    result -= num
                elif op == "*":
                    result *= num
                elif op == "/":
                    if num == 0:
                        await ctx.reply("❌ Can't divide by zero!")
                        return
                    result /= num

            await ctx.send(f"🧮 {expression} = {result}")

        except ValueError:
            await ctx.reply("❌ Invalid numbers!")
