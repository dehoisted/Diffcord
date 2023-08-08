import discord
import os
import json
import random
import time
import asyncio
from utils.utils import debug_print
from discord.ext import commands

class BotClient(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        intents = discord.Intents.all()
        super().__init__(command_prefix=',', intents=intents, **kwargs)
        self.remove_command('help')

        if not os.path.exists('data.json'):
            with open('data.json', 'w') as f:
                json.dump({}, f, indent=4)

    async def load_cogs(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                debug_print(f"loaded cog: {filename[:-3]}")

    async def on_ready(self):
        await self.load_cogs()
        debug_print("bot is ready")
        # Change bot status
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=",help"), status=discord.Status.online)

    async def on_command(self, ctx):
        debug_print(f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) sent command: {ctx.command.name}")

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        error = getattr(error, 'original', error)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"**{ctx.command.name}** command's arguments: {ctx.command.signature}")
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            msg = await ctx.send(f"Be cool and retry in **{error.retry_after:.0f} seconds 😎**")
            await asyncio.sleep(2.5)
            await msg.delete()
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I do not have permission to use this command")
        else:
            await ctx.send("Fatal error, report this to the dev: " + str(error))
            debug_print(str(error))

def main():
    bot = BotClient(shard_count=1, help_command=None)
    bot.run('token')

if __name__ == "__main__":
    main()
