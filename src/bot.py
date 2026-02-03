import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from markov import MarkovChain


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
markov = MarkovChain()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()

    markov.train(content)
    await bot.process_commands(message)


@bot.command(name="m")
async def markov_command(ctx):
    reply = markov.generate()
    if reply:
        await ctx.send(reply)
    else:
        await ctx.send("Not enough data :(")


token = os.getenv("TOKEN")
bot.run(token)
