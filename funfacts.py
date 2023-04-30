import requests
import os
import random
import discord
import AllCountries
from discord.ext import commands, tasks

base_url = "https://restcountries.com/v3.1/all"

resp = requests.get(base_url)

data = resp.json()

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    if message.channel.id == 1102037939900395571:
        if message.content.startswith('!get_country_info'):
            await message.channel.send("What country would you like to know about?")

            def check(msg):
                return msg.author == message.author and msg.channel == message.channel

            reply = await bot.wait_for('message', check=check)
            country_name = reply.content

            for country_data in data:
                if country_data['name']['common'].lower() == country_name.lower():
                    capital = country_data['capital'][0]
                    region = country_data['region']
                    subregion = country_data['subregion']
                    population = country_data['population']
                    languages = ', '.join(country_data['languages'].keys())
                    currency = ', '.join(country_data['currencies'].keys())

                    fun_facts = [
                        f"Did you know that {country_name} is home to over {population} people?",
                        f"The capital city of {country_name} is {capital}.",
                        f"{country_name} is located in the {subregion} region of {region}.",
                        f"The official languages of {country_name} are {languages}.",
                        f"{country_name} uses {currency} as its official currency."]
                    await message.channel.send(random.choice(fun_facts))
                    break
            else:
                await message.channel.send(f"I'm sorry, I couldn't find any information for {country_name}.")

    await bot.process_commands(message)

my_secret = os.environ['DISCORD_BOT_SECRET']
bot.run(my_secret)
























# import requests
# import os
# import random
# import discord
# import AllCountries
# from discord.ext import commands, tasks

# base_url = "https://restcountries.com/v3.1/all"

# resp = requests.get(base_url)

# data = resp.json()

# intents = discord.Intents.all()
# intents.message_content = True

# bot = commands.Bot(command_prefix='!', intents=intents)

# @bot.command()
# async def get_country_info(ctx):
#     await ctx.send("What country would you like to know about?")

#     def check(msg):
#         return msg.author == ctx.author and msg.channel == ctx.channel

#     message = await bot.wait_for('message', check=check)
#     country_name = message.content

#     for country_data in data:
#         if country_data['name']['common'].lower() == country_name.lower():
#             capital = country_data['capital'][0]
#             region = country_data['region']
#             subregion = country_data['subregion']
#             population = country_data['population']
#             languages = ', '.join(country_data['languages'].keys())
#             currency = ', '.join(country_data['currencies'].keys())

#             fun_facts = [
#                 f"Did you know that {country_name} is home to over {population} people?",
#                 f"The capital city of {country_name} is {capital}.",
#                 f"{country_name} is located in the {subregion} region of {region}.",
#                 f"The official languages of {country_name} are {languages}.",
#                 f"{country_name} uses {currency} as its official currency."]
#             await ctx.send(random.choice(fun_facts))
#             break
#     else:
#         await ctx.send(f"I'm sorry, I couldn't find any information for {country_name}.")


# my_secret = os.environ['DISCORD_BOT_SECRET']
# bot.run(my_secret)
