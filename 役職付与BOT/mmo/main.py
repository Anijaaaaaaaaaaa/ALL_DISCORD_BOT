import discord
import aiomysql
import threading
import asyncio
from discord.ext import commands
counts = {}
start_count = []


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def makuros(self, cur, conn, message, bot):
        user_id = message.author.id
        if user_id not in counts:
            counts[user_id] = 0
        try:
            process_list = [bot.wait_for('message', check=lambda messages: messages.author.id == user_id, timeout=3), ]
            message1, pending_tasks = await asyncio.wait(process_list, return_when=asyncio.FIRST_COMPLETED)
            if [t.result() for t in message1][0] and [t.result() for t in message1][0].content:
                counts[user_id] += 1
                if counts[user_id] >= 7:
                    await cur.execute("INSERT INTO get VALUES(%s);", (user_id,))
                    await conn.commit()
                    embed = discord.Embed(description=f"{message.author.mention}さんはスパムをしたためこのチャンネルで発言できません。")
                    try:
                        return await asyncio.gather(*(c.send(embed=embed) for c in bot.get_all_channels() if c.name == 'tao-global'))
                    except Exception as _:
                        pass

        except asyncio.TimeoutError:
            if user_id in counts:
                del counts[user_id]
            return

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            return

        if message.channel.name == "tao-global":
            if message.author == self.bot.user or message.author.bot and message.author.id != 526620171658330112 or message.author.id in start_count:
                return

            loops = asyncio.get_event_loop()
            pool = await aiomysql.create_pool(host='127.0.0.1', user='root', password='', db='role', loop=loops)
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    start_count.append(message.author.id)
                    thread = threading.Thread(target=await self.makuros(cur, conn, message, self.bot))
                    thread.start()
                    thread.join()
                    start_count.remove(message.author.id)

            pool.close()
            await pool.wait_closed()


def setup(bot):
    bot.add_cog(Main(bot))
