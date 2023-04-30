import requests
import os
import discord
import random
import asyncio
from discord.ext import commands, tasks

base_url = "https://restcountries.com/v3.1/all"

resp = requests.get(base_url)

data = resp.json()

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("first Bot is ready!")
    
    # Get the channel object
    channel2 = bot.get_channel(1101662911031685152)
    
    # Check if the message has already been sent
    messages = [msg async for msg in channel2.history(limit=1)]
    if messages and messages[0].embeds and messages[0].embeds[0].title == "Welcome! Enter '!play_round' to begin":
        return
    
    # Create and send the embed message
    embed = discord.Embed(title="Welcome! Enter '!play_round' to begin", color=discord.Color.green())
    await channel2.send(embed=embed)


def random_number():
  randint = random.randint(0, 249)
  return randint


async def get_country(ctx, num: int):
  res = requests.get(base_url)
  resJSON = res.json()
  country = resJSON[num]["name"]["common"]
  return country


async def get_capital(ctx, num: int):
  res = requests.get(base_url)
  resJSON = res.json()
  get_cap = resJSON[num]["capital"]
  return get_cap[0]


async def get_country_img(ctx, num: int):
  res = requests.get(base_url)
  resJSON = res.json()
  get_img = resJSON[num]["flags"]["png"]
  return get_img


#@bot.command()
#async def country_flag_gss(ctx):
#ctry = await get_country(ctx)
#img = await get_country_img(ctx)
#await ctx.send("Guess the country based on the flag")


@bot.command()
async def play_round(ctx):

  # channel = bot.get_channel(1101662911031685152)
  await ctx.send("Let's play!")
  print("TEST")
  score = 0
  # game = CapitalGuess(score)

  b = True

  while b:
    rand_number = random_number()
    ctry = await get_country(ctx, rand_number)
    cap = await get_capital(ctx, rand_number)
    img = await get_country_img(ctx, rand_number)
    await ctx.send("What is the captial of " + str(ctry) + "?")
    await ctx.send(img)
    try:
      response = await bot.wait_for(
        "message",
        check=lambda message: message.author == ctx.author and message.
        channel == ctx.channel,
        timeout=25.0)

      while cap.lower() != response.content.lower():

        if response.content.lower() != cap.lower(
        ) and b != False and response.content.lower() != "quit":
          await ctx.send("You got it wrong! try again")

          try:
            response = await bot.wait_for(
              "message",
              check=lambda message: message.author == ctx.author and message.
              channel == ctx.channel,
              timeout=60.0)
          except asyncio.TimeoutError:
            # handle the timeout here
            await ctx.send("You ran out of time!")
            break
            return

        else:
          break

      if response.content.lower() == "quit":
        await ctx.send("Thanks for playing!")
        b = False
        break

      await ctx.send("Congrats, you got it right")
      score += 1
      await ctx.send("Your score is now: " + str(score))
      if b == False:
        break
      else:
        continue
    except asyncio.TimeoutError:
      await ctx.send("You ran out of time!")
      await ctx.send("Thanks for playing!")
      break
      return


my_secret = os.environ['DISCORD_BOT_SECRET']
bot.run(my_secret)
