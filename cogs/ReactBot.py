from discord.ext import commands
import discord
import json
import os
import config

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
        if '!reactbot!' in message.content and message.author.id == config.ADMINID:
            botmsg = await message.channel.send('Reactions!')
            self.watchedMessages[message.id] = botmsg.id
            self.save()
            # add message to watched messages
            # link user message with bot messages

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



'''
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member == self.bot.user:
            return
        elif payload.message_id in self.watchedMessages:
            r = discord.utils.get(payload.member.guild.roles, id = self.watchedMessages[payload.message_id][str(payload.emoji)])
            await payload.member.add_roles(r)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id in self.watchedMessages:
            g = self.bot.get_guild(payload.guild_id)
            m = g.get_member(payload.user_id)
            r = discord.utils.get(g.roles, id = self.watchedMessages[payload.message_id][str(payload.emoji)])
            await m.remove_roles(r)
'''

    # @commands.command()
    # async def createAssignMsg(self, ctx, *args):
    #     msg = await ctx.send('React to get the following roles!')
    #     self.watchedMessages[msg.id] = {}
    #     for i in range(1, len(args), 2):
    #         await msg.add_reaction(args[i])
    #         self.watchedMessages[msg.id][args[i]] = int(args[i-1][3:-1])
    #
    #     await self.editmessage(msg)
    #     self.save()
    #
    # async def editmessage(self, msg):
    #     s = 'React to get the following roles!'
    #     for e in self.watchedMessages[msg.id]:
    #         r = discord.utils.get(msg.guild.roles, id = self.watchedMessages[msg.id][e])
    #         s += '\n{} : {}'.format(e, r.mention)
    #     await msg.edit(content = s)
    #
    #
    # @commands.command()
    # async def addRole(self, ctx, *args):
    #     msg = await ctx.channel.history().get(author = self.bot.user)
    #     for i in range(1, len(args), 2):
    #         await msg.add_reaction(args[i])
    #         self.watchedMessages[msg.id][args[i]] = int(args[i-1][3:-1])
    #     await self.editmessage(msg)
    #
    # @commands.command()
    # async def removeRole(self, ctx, *args):
    #     msg = await ctx.channel.history().get(author = self.bot.user)
    #     for e in args:
    #         del self.watchedMessages[msg.id][e]
    #         await msg.clear_reaction(e)
    #     await self.editmessage(msg)
