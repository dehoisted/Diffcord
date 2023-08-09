import discord
import json
import random
import time
import asyncio
from utils.utils import debug_print
from discord.ext import commands

class BotMain(commands.Cog):

    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
    
    @commands.command()
    @commands.cooldown(1, 50, commands.BucketType.user)
    async def shards(self, ctx):
        embed = discord.Embed(title="Shards", description=None, color=0x2F3136)
        for shard in self.bot.shards:
            s = self.bot.get_shard(shard)
            embed.add_field(name=f"Shard {s.id}", value=f"`latency: {str(s.latency)}ms` (measure time between heartbeats)", inline=True) # FIX-THIS: give a proper reading
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        msg = await ctx.send("**Read the docs: <>**") # Implement help menu embed?
        await asyncio.sleep(10)
        await msg.delete()

async def setup(client):
    debug_print("setting up bot cog")
    random.seed(time.time())

    with open('data.json', 'r') as f:
        data = json.load(f)
    try:
        await client.add_cog(BotMain(client, data))
    except Exception as e:
        debug_print("error setting up bot cog")
        print(e)
