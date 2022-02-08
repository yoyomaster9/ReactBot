from discord.ext import commands
import discord
import json
import os

# Requires message intent for role remove

class React(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load()

    def save(self):
        with open('watchedMessages.json', 'w') as fp:
            json.dump(self.watchedMessages, fp, indent=4)

    def load(self):
        if os.path.exists('watchedMessages.json'):
            with open('watchedMessages.json', 'r') as fp:
                self.watchedMessages = json.load(fp)
                self.watchedMessages = {int(x):self.watchedMessages[x] for x in self.watchedMessages}
        else:
            self.watchedMessages = {}
            self.save()


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if '!reactbot!' in message.content:
            botmsg = await message.channel.send('Reactions!')
            self.watchedMessages[message.id] = botmsg.id
            self.save()

    @commands.command()
    async def watch(self, ctx, msg_id):
        msg_id = int(msg_id)
        botmsg = await ctx.channel.send('Reactions!')
        self.watchedMessages[msg_id] = botmsg.id
        self.save()

    @commands.command()
    async def unwatch(self, ctx, msg_id):
        msg_id = int(msg_id)
        try:
            bot_msg_id = self.watchedMessages[msg_id]
            bot_msg = await ctx.channel.fetch_message(bot_msg_id)
            await bot_msg.delete()
        except discord.errors.NotFound:
            await ctx.send('Message not found! Maybe in different channel?')
        except KeyError:
            await ctx.send('Message isn\'t being watched!')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id in self.watchedMessages:
            await self.updateReactMsg(payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id in self.watchedMessages:
            await self.updateReactMsg(payload)

    async def updateReactMsg(self, payload):
        channel_id = payload.channel_id
        bot_msg_id = self.watchedMessages[payload.message_id]

        channel = self.bot.get_channel(channel_id)
        author_msg = await channel.fetch_message(payload.message_id)
        bot_msg = await channel.fetch_message(bot_msg_id)


        s = 'Reactions!'
        for r in author_msg.reactions:
            users = await r.users().flatten()
            temp = ', '.join([x.mention for x in users])
            s += f'\n {r}: {temp}' # maybe try *users if not unpacked?

        await bot_msg.edit(content = s)
