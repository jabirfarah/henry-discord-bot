import os
import discord
import AllCountries
import funfacts
import guessCapital
import requests
import os
import discord
import random
import asyncio

guessCapital_channel_id = 1101662911031685152
funfacts_channel_id = 1102037939900395571
countries_channel_id = 1102025012740898896

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

bot.add_command(guessCapital)
bot.add_command(guessCapital.get_fun_fact)

my_secret = os.environ['DISCORD_BOT_SECRET']
bot.run(my_secret)
