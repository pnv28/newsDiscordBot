import discord
import logging
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
import os
import requests
import random

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

activity = discord.Activity(name='news', type=discord.ActivityType.watching)

bot = discord.Bot(activity=activity)
id = 1150701854557220927

@bot.event
async def on_ready():
  print(f"{bot.user} is read to go!")

@bot.slash_command(name= "ping", description= "Responds with Pong!")
async def ping(ctx):
  await ctx.respond(f"Pong! Latency is {round(bot.latency * 1000)} ms")

@bot.slash_command(name= "news", description= "top news")
async def news(ctx):
  n = random.randrange(0, 19, 3)
  response = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=41009e7f277149fd8b6d6e3692b7c1ed")
  title = response.json()["articles"][n]["title"]
  snippet = response.json()["articles"][n]["description"]
  url = response.json()["articles"][n]["url"]
  imgUrl = response.json()["articles"][n]["urlToImage"]
  source = response.json()["articles"][n]["source"]["name"]
  author = response.json()["articles"][n]["author"]
  newsEmbed = discord.Embed(
    title=f"{title}",
    description=f"{snippet}\n[Read More]({url})",
    color=discord.Color.green()
  )
  newsEmbed.set_image(url=imgUrl)
  newsEmbed.set_footer(text=f"Source: {source}")
  newsEmbed.set_author(name=author)
  await ctx.respond(embed = newsEmbed)

@bot.slash_command(name="start_news", description="Starts the news loop")
async def start_news(ctx):
  if ( ctx.author.id == 389306174119608321 ) or ( ctx.author.id == 925231204104568953):
    await ctx.respond("Starting news loop...")
    newsPeriodic.start()
  else:
    await ctx.respond("You are not authorized to use this command.")

"""@bot.slash_command(name="stop_news", description="Stops the news loop")
async def stop_news(ctx):
  if ( ctx.author.id == 389306174119608321 ) or ( ctx.author.id == 925231204104568953):
    await ctx.response("Stopping news loop...")
    newsPeriodic.cancel()
  else:
    await ctx.respond("You are not authorized to use this command.")"""

@tasks.loop(minutes=30)
async def newsPeriodic():
  n = random.randrange(0, 19, 3)
  response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={os.getenv(NEWS_API)}")
  title = response.json()["articles"][n]["title"]
  snippet = response.json()["articles"][n]["description"]
  url = response.json()["articles"][n]["url"]
  imgUrl = response.json()["articles"][n]["urlToImage"]
  source = response.json()["articles"][n]["source"]["name"]
  author = response.json()["articles"][n]["author"]
  newsEmbed = discord.Embed(
    title=f"{title}",
    description=f"{snippet}\n[Read More]({url})",
    color=discord.Color.green()
  )
  newsEmbed.set_image(url=imgUrl)
  newsEmbed.set_footer(text=f"Source: {source}")
  newsEmbed.set_author(name=author)
  channel = bot.get_channel(id)
  print(id)
  if channel is not None:
      await channel.send(embed = newsEmbed)


bot.run(os.getenv("TOKEN"))