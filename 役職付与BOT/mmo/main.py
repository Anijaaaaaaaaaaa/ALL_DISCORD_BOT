import discord
import aiomysql
import asyncio
from discord.ext import commands
counts = {}


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            return
        
        if message.channel.name == "tao-global":
            if message.author == self.bot.user or message.author.bot and not message.author.id == 526620171658330112:
                return

            user_id = message.author.id
            if user_id not in counts:
                counts[user_id] = 0
            try:
                check = await self.bot.wait_for('message', check=lambda messages: messages.author.id == user_id, timeout=4)
                if check:
                    counts[user_id] += 1
                    if counts[user_id] >= 7:
                        async with aiomysql.connect(host="localhost", user="root", db="role", password="") as conn:
                            async with conn.cursor() as cur:
                                await cur.execute("INSERT INTO get VALUES(%s);", (user_id,))
                                await conn.commit()
                                embed = discord.Embed(description=f"{message.author.mention}さんはスパムをしたためこのチャンネルで発言できません。")
                                return await asyncio.gather(*(c.send(embed=embed) for c in self.bot.get_all_channels() if c.name == 'tao-global'))
                                
            except asyncio.TimeoutError:
                if user_id in counts:
                    del counts[user_id]


def setup(bot):
    bot.add_cog(Main(bot))
