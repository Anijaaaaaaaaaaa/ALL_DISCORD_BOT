import asyncio
import discord
import random
import aiomysql
import json
from discord.ext import commands

with open(r'setting.json', mode='r', encoding='utf-8') as fh:
    json_txt = fh.read()
    json_txt = str(json_txt).replace("'", '"').replace('True', 'true').replace('False', 'false')
    token = json.loads(json_txt)['token']
    prefix = json.loads(json_txt)['prefix']
on_ready_complete = []


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
        for cog in ['mmo.mmo_bot', 'mmo.main']:
            self.load_extension(cog)

        await self.change_presence(activity=discord.Game(name=f"{prefix}help"))
        on_ready_complete.append("ok")
        await self.get_channel(550674420222394378).edit(name=f"総メッセージ数: 5708501")

    async def on_member_join(self, member):
        if not member.guild.id == 337524390155780107 or self.user == member:
            return        
        up = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(title=f"{member.name}さんがこの鯖に入りました！～", description=f"現在の鯖の人数: `{len(member.guild.members)}人`\n{member.mention}さんに役職を付与しました。", color=up)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
        await self.get_channel(338173860719362060).send(embed=embed)
        await self.get_channel(537227342104494082).edit(name=f"総メンバー数: {len(member.guild.members)}")
        await self.get_channel(537227343207333888).edit(name=f"ユーザー数: {len([member for member in member.guild.members if not member.bot])}")
        await self.get_channel(537227343844868096).edit(name=f"ボットの数: {len([member for member in member.guild.members if member.bot])}")

        async with aiomysql.connect(host="localhost", user="root", db="role", password="") as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM get_role WHERE author_id=%s;", (member.id,))
                for row in await cur.fetchall():
                    role = discord.utils.get(member.guild.roles, id=row[1])
                    await member.add_roles(role)

                await cur.execute("delete from get_role where author_id=%s;", (member.id,))
                await conn.commit()

    async def on_member_remove(self, member):
        if not member.guild.id == 337524390155780107:
            return
        embed = discord.Embed(title="ありがとうございました！", description=f"{member.name}さんが\nこの鯖から退出しました...；；\n\n現在の鯖の人数: `{len(member.guild.members)}人`")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
        await self.get_channel(338173860719362060).send(embed=embed)
        await self.get_channel(537227342104494082).edit(name=f"総メンバー数: {len(member.guild.members)}")
        await self.get_channel(537227343207333888).edit(name=f"ユーザー数: {len([member for member in member.guild.members if not member.bot])}")
        await self.get_channel(537227343844868096).edit(name=f"ボットの数: {len([member for member in member.guild.members if member.bot])}")

        async with aiomysql.connect(host="localhost", user="root", db="role", password="") as conn:
            async with conn.cursor() as cur:
                for role in member.roles:
                    if "@everyone" not in role.name:
                        await cur.execute("INSERT INTO get_role VALUES(%s,%s);", (member.id, role.id))
                        await conn.commit()

    async def on_command_error(self, ctx, error):
        if not on_ready_complete:
            return await ctx.send(f"{ctx.message.author.mention}\n```『{self.user.name}』は現在再起動中.....```")
        try:
            if isinstance(error, commands.CommandNotFound):
                msg = discord.Embed(description=f"{ctx.message.author.mention}さん\n{ctx.message.content}というコマンドはありません！", color=0xC41415)
                return await ctx.send(embed=msg)
            elif isinstance(error, commands.CommandOnCooldown):
                msg = discord.Embed(description='{}さん！\nこのコマンドは{:.2f}秒後に使用可能です！'.format(ctx.message.author.mention, error.retry_after), color=0xC41415)
                return await ctx.send(embed=msg)
            elif isinstance(error, commands.MissingPermissions):
                msg = discord.Embed(description=f"{ctx.message.author.mention}さん\nあなたはこのコマンドを使用するには権限がありません！", color=0xC41415)
                return await ctx.send(embed=msg)
            
        except discord.Forbidden:
            pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
