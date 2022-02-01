import discord
from discord.ext import commands
import config
import cogs

BOT_PREFIX = ('/')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents = intents)
for x in commands.Cog.__subclasses__():
    bot.add_cog(x(bot))

@bot.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == bot.user:
        return

    # Only used for admins
    elif message.author.id != config.ADMINID:
        return

    else:
        await bot.process_commands(message)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Add !reactbot! track messages'))
    print('Logged in as ' + bot.user.name)
    print('---------------------')
    print(f'Logged into servers: {[x.name for x in bot.guilds]}')


bot.run(config.discordtoken)
