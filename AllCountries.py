import requests
import os
import discord
from discord.ext import commands, tasks

base_url = "https://restcountries.com/v3.1/all"

resp = requests.get(base_url)

data = resp.json()

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Second Bot is ready!")
    
    # Get the channel object
    channel = bot.get_channel(1102025012740898896)
    
    # Check if the message has already been sent
    messages = [msg async for msg in channel.history(limit=1)]
    if messages and messages[0].embeds and messages[0].embeds[0].title == "Welcome! Enter '!start_game' to begin":
        return
    
    # Create and send the embed message
    embed = discord.Embed(title="Welcome! Enter '!start_game' to begin", color=discord.Color.green())
    await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('!start_game'):
        score = 0
        embed = discord.Embed(title="Guess as many countries as you can.", color=discord.Color.green())
        embed.set_footer(text="Enter 'done' when you're done.")
        await message.channel.send(embed=embed)
        while True:
            response = await bot.wait_for('message', check=lambda m: m.author == message.author)
            if response.content.lower() == 'done':
                await message.channel.send(f"🏁 Your final score is {score}")
                break
            for country in data:
                if response.content.lower() == country['name']['common'].lower():
                    score += 1
                    embed = discord.Embed(title=f"👍 You got {score}!", color=discord.Color.green())
                    await message.channel.send(embed=embed)
                    break
            else:
                embed = discord.Embed(title="👎 That's incorrect. Try again!", color=discord.Color.red())
                await message.channel.send(embed=embed)

my_secret = os.environ['DISCORD_BOT_SECRET']
bot.run(my_secret)
