import discord
from discord.ext import commands
import config

BOT_PREFIX = ('/')

client = commands.Bot(command_prefix=BOT_PREFIX)
# client = commands.Bot()


@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

    # Only used for admins
    elif message.author.id != config.ADMINID:
        return

    else:
        await client.process_commands(message)



@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command(brief = 'Logs bot out of all servers [ADMIN ONLY]',
                description = 'Logs bot out of all servers [ADMIN ONLY]')
async def logout(ctx):
    await ctx.send('Goodbye!')
    await client.close()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Add !react to end'))
    print('Logged in as ' + client.user.name)
    print('---------------------')
    print(f'Logged into servers: {[x.name for x in client.guilds]}')


client.run(config.discordtoken)
