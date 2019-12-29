import discord
import sqlite3
import asyncio
import json
from discord.ext import commands

with open(r'setting.json', mode='r', encoding='utf-8') as fh:
    json_txt = fh.read()
    json_txt = str(json_txt).replace("'", '"').replace('True', 'true').replace('False', 'false')
    token = json.loads(json_txt)['token']
    prefix = json.loads(json_txt)['prefix']


async def run():
    bot = MyBot()
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        await bot.logout()


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(prefix))
        self.remove_command('help')

    async def on_ready(self):
        for cog in ['cogs.help', 'cogs.spam_everyone', 'cogs.webhook']:
            self.load_extension(cog)
        await self.change_presence(activity=discord.Game(name=f"現在{len(self.guilds)}鯖と同期中"))

    async def on_member_join(self, member):
        if member.guild.id == 657756673410334724:
            with sqlite3.connect('chat.db') as conn:
                co = conn.cursor()
                co.execute("SELECT * FROM get_role WHERE author_id=?", (member.id,))
                for row in co.fetchall():
                    role = discord.utils.get(member.guild.roles, id=int(row[1]))
                    await member.add_roles(role)
                    await asyncio.sleep(1)
    
                co.execute("delete from get_role where author_id=?", (member.id,))
                conn.commit()

    async def on_member_remove(self, member):
        if member.guild.id == 657756673410334724:
            with sqlite3.connect('chat.db') as conn:
                co = conn.cursor()
                for role in member.roles:
                    if "@everyone" not in role.name:
                        co.execute("INSERT INTO get_role(author_id, role_id) VALUES(?,?)", (member.id, role.id))
                        conn.commit()
        
    async def on_guild_remove(self, _):
        await self.change_presence(activity=discord.Game(name=f"現在{len(self.guilds)}鯖と同期中"))

    async def on_guild_join(self, _):
        await self.change_presence(activity=discord.Game(name=f"現在{len(self.guilds)}鯖と同期中")) 


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
