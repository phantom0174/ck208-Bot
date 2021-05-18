from discord.ext import commands
import discord
import sys
import os
import keep_alive
import asyncio


intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix='!!',
    intents=intents,
    case_insensitive=True,
    owner_id=610327503671656449
)


@bot.event
async def on_ready():
    print("\ Bot is online /")


@bot.command()
async def reload(ctx):
    for reload_filename in os.listdir('./cogs'):
        if reload_filename.endswith('.py'):
            bot.reload_extension(f'cogs.{reload_filename[:-3]}')

    await ctx.send(':white_check_mark: Reload finished!')


@bot.command(aliases=['logout', 'shutdown'])
async def shut_down(ctx):
    await ctx.send(':white_check_mark: The bot is shutting down...')
    await bot.logout()
    await asyncio.sleep(1)
    sys.exit(0)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


keep_alive.keep_alive()

if __name__ == "__main__":
    bot.run(os.environ.get("TOKEN"))
