import discord
import re
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get_role")
    async def get_role(self, ctx):
        if ctx.message.channel.id == 657789033564471299:
            role = discord.utils.get(ctx.message.guild.roles, id=657907350975414273)
            await ctx.message.author.add_roles(role)
            await ctx.send(f"『{role}』役職を{ctx.message.author.mention}さんに付与しました。")
            await ctx.message.author.send(f"{ctx.message.author.mention}さん\n{self.bot.get_channel(657778204316008469).mention}だけは絶対読んでください。")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.webhook_id:
            return
        if isinstance(message.channel, discord.DMChannel):
            return
        
        if message.guild.id == 657756673410334724:
            if message.channel.id != 657789033564471299 and message.content.startswith("&get_role"):
                await message.delete()
                await message.channel.send(f"{message.author.mention}さん\nこのコマンドはこのチャンネルでは使えません。")
                
            if message.channel.id == 657789033564471299 and not message.content.startswith("&get_role") and message.author != self.bot.user:
                return await message.delete()
                
            if message.channel.id == 657769986303066113:
                error_server, error_url = [], []
                url = re.findall("discord.gg/([a-zA-Z1-9]+)", message.content)
                if not url:
                    await message.delete()
                    await message.author.send(f"{message.author.mention}さん！\nここのチャンネルでは『discord.gg/』LINKの鯖しか対応してないよ！\nもう一度{self.bot.get_channel(657778204316008469).mention}を読んでくれよな！")
                else:
                    for i in url:
                        try:
                            invite = await self.bot.fetch_invite(i)
                            guild_members = [member for member in invite.guild.members if not member.bot]
                            all_member = len(guild_members)
                            if invite.guild.owner_id == message.author.id:
                                if 1 <= all_member <= 100:
                                    role = discord.utils.get(message.guild.roles, name=f"Lv.1 Server Owner (User:1~100)")
                                elif 101 <= all_member <= 250:
                                    role = discord.utils.get(message.guild.roles, name=f"Lv.2 Server Owner (User:101~250)")
                                elif 201 <= all_member <= 500:
                                    role = discord.utils.get(message.guild.roles, name=f"Lv.3 Server Owner (User:251~500)")
                                elif 501 <= all_member <= 1000:
                                    role = discord.utils.get(message.guild.roles, name=f"Lv.4 Server Owner (User:501~1000)")
                                elif 1001 <= all_member <= 1500:
                                    role = discord.utils.get(message.guild.roles, name=f"Lv.5 Server Owner (User:1001~1500)")
                                elif 1501 <= all_member <= 2000:
                                    role = discord.utils.get(message.guild.roles, name=f"Lv.6 Server Owner (User:1501~2000)")
                                elif 2001 <= all_member <= 3000:
                                    role = discord.utils.get(message.guild.roles, name=f"Lv.7 Server Owner (User:2001~3000)")
                                elif 3001 <= all_member <= 5000:
                                    role = discord.utils.get(message.guild.roles, name=f"Lv.8 Server Owner (User:3001~5000)")
                                elif 5001 <= all_member <= 7500:
                                    role = discord.utils.get(message.guild.roles, name=f"Lv.9 Server Owner (User:5001~7500)")
                                elif 7501 <= all_member <= 10000:
                                    role = discord.utils.get(message.guild.roles, name=f"Lv.10 Server Owner (User:7501~10000)")
                                else:
                                    role = discord.utils.get(message.guild.roles, name=f"Lv.∞ Server Owner (User:10001~)")
                                await message.author.add_roles(role)
                                
                            else:
                                for user in guild_members:
                                    if message.author == user:
                                        for admin_role in user.roles:
                                            if admin_role.permissions.administrator:
                                                if 1 <= all_member <= 100:
                                                    role = discord.utils.get(message.guild.roles, name=f"Lv.1 Server Admin (User:1~100)")
                                                elif 101 <= all_member <= 250:
                                                    role = discord.utils.get(message.guild.roles, name=f"Lv.2 Server Admin (User:101~250)")
                                                elif 201 <= all_member <= 500:
                                                    role = discord.utils.get(message.guild.roles, name=f"Lv.3 Server Admin (User:251~500)")
                                                elif 501 <= all_member <= 1000:
                                                    role = discord.utils.get(message.guild.roles, name=f"Lv.4 Server Admin (User:501~1000)")
                                                elif 1001 <= all_member <= 1500:
                                                    role = discord.utils.get(message.guild.roles, name=f"Lv.5 Server Admin (User:1001~1500)")
                                                elif 1501 <= all_member <= 2000:
                                                    role = discord.utils.get(message.guild.roles, name=f"Lv.6 Server Admin (User:1501~2000)")
                                                elif 2001 <= all_member <= 3000:
                                                    role = discord.utils.get(message.guild.roles, name=f"Lv.7 Server Admin (User:2001~3000)")
                                                elif 3001 <= all_member <= 5000:
                                                    role = discord.utils.get(message.guild.roles, name=f"Lv.8 Server Admin (User:3001~5000)")
                                                elif 5001 <= all_member <= 7500:
                                                    role = discord.utils.get(message.guild.roles, name=f"Lv.9 Server Admin (User:5001~7500)")
                                                elif 7501 <= all_member <= 10000:
                                                    role = discord.utils.get(message.guild.roles, name=f"Lv.10 Server Admin (User:7501~10000)")
                                                else:
                                                    role = discord.utils.get(message.guild.roles, name=f"Lv.∞ Server Admin (User:10001~)")
                                                await message.author.add_roles(role)
                                
                        except AttributeError:
                            invite = await self.bot.fetch_invite(i)
                            error_server.append(f"`{invite.guild.name}`")
                        
                        except discord.errors.NotFound:
                            error_url.append(f"`discord.gg/{i}`")
                    
                    if error_url or error_server:
                        if error_server:
                            guilds = "".join([f'{guild}, ' for guild in error_server])
                            await message.author.send(f"{message.author.mention}さん！\nこのBOTが[{guilds[:-2]}]で入ってないよ！")
                            
                        if error_url:
                            invites = "".join([f'{invites}, ' for invites in error_url])
                            await message.author.send(f"{message.author.mention}さん！\n[{invites[:-2]}]は無効な招待だよ！")
                        await message.delete()
            else:
                try:
                    if any([True for s in ["DISCORD.GG", "DISBOARD.ORG", "BIT.LY", "DISCORDAPP", "INVITE.GG", "DISCORD.COM"] if s in message.content.upper()]) and message.author.id != 304932786286886912:
                        channel = self.bot.get_channel(657769986303066113)
                        embed = discord.Embed(title="このチャンネルでは宣伝は禁止です！", description="{0}さん\nもし鯖の宣伝をしたいなら{1}でやってください！".format(message.author.mention, channel.mention))
                        await message.author.send(embed=embed)  
                        return await message.delete()
                except discord.errors.HTTPException:
                    pass
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            if before.guild.id == 657756673410334724:
                if any([True for s in ["DISCORD.GG", "DISBOARD.ORG", "BIT.LY", "DISCORDAPP", "INVITE.GG", "DISCORD.COM"] if s in after.content.upper()]) and not before.author.bot and before.channel.id != 657769986303066113:
                    channel = self.bot.get_channel(657769986303066113)
                    embed = discord.Embed(title="このチャンネルでは宣伝は禁止です！", description="{0}さん\nもし鯖の宣伝をしたいなら{1}でやってください！".format(after.author.mention, channel.mention))
                    await after.author.send(embed=embed)  
                    return await after.delete()
        except AttributeError:
            pass


def setup(bot):
    bot.add_cog(Help(bot))
