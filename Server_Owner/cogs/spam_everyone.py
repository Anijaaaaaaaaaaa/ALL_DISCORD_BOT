import time
import discord
import sqlite3
from discord.ext import commands

check = []


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.webhook_id:
            return
        
        if isinstance(message.channel, discord.DMChannel):
            return
        
        if message.guild.id == 657756673410334724:
            if (len(message.raw_mentions) >= 3 or any([True for s in ["@everyone", "@here"] if s in message.content])) and message.author.id not in check:
                check.append(message.author.id)
                t0 = time.time()
                count = 1
                while time.time() - t0 < 10:
                    react = await self.bot.wait_for('message', check=lambda messages: messages.author == message.author)
                    if react and (len(react.raw_mentions) >= 3 or any([True for s in ["@everyone", "@here"] if s in react.content])):
                        if count >= 5:
                            role = discord.utils.get(message.guild.roles, id=657777429783380021)
                            if role in message.author.roles:
                                await message.author.ban()
                                check.remove(message.author.id)
                                return await message.channel.send(f"{message.author.mention}さんをスパム検知でBANしました。")
    
                            with sqlite3.connect('chat.db') as conn:
                                co = conn.cursor()
                                co.execute("INSERT INTO ban_list values(?)", (message.author.id,))
                                conn.commit()
    
                            check.remove(message.author.id)
                            await message.author.add_roles(role)
                            return await message.channel.send(f"{message.author.mention}さん！\nスパム検知しました。")
                        count += 1
                    else:
                        return check.remove(message.author.id)


def setup(bot):
    bot.add_cog(User(bot))
