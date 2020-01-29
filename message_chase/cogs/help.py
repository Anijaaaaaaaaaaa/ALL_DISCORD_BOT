import re

import discord
from discord.ext import commands
from datetime import datetime


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', pass_context=True, hidden=True)
    @commands.bot_has_permissions(read_messages=True, send_messages=True, embed_links=True, read_message_history=True)
    async def helps(self, ctx):
        try:
            invite = "https://discordapp.com/api/oauth2/authorize?client_id=643872330325557260&permissions=117760&scope=bot"
            timestamp = datetime.utcfromtimestamp(int(self.bot.user.created_at.timestamp()))
            embed = discord.Embed(title="Chase Message URL's Help:", description=f">>> ```Send Message URL to Channel.```[Invite From Here](<{invite}>)", timestamp=timestamp)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.add_field(name="Amount Server", value=f"`{len(self.bot.guilds)}`")
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name="Amount User", value=f"`{len(set(self.bot.get_all_members()))}`")
            embed.add_field(name="Library", value="`discord.py`")
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name="Bot Latency", value=f"`{self.bot.ws.latency * 1000:.0f}ms`")
            embed.set_footer(text="This BOT Created")
            return await ctx.send(embed=embed)

        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(description=f"Hey,{ctx.message.author.mention}\nI can't that channel message...\nI think I don't have permission to chase that message...", colour=discord.Color.dark_red()))

    @commands.Cog.listener()
    @commands.bot_has_permissions(read_messages=True, send_messages=True, embed_links=True, read_message_history=True)
    async def on_message(self, message):
        if re.findall("https?://discordapp.com/channels/[0-9]+/[0-9]+/[0-9]+", message.content):
            for message_url in re.findall("https?://discordapp.com/channels/[0-9]+/[0-9]+/[0-9]+", message.content):
                global messagess
                messagess = ""
                while True:
                    if not messagess:
                        messagess = message_url

                    if "@me" in messagess:
                        await message.channel.send(embed=discord.Embed(description=f"Hey,{message.author.mention}\nI can't chase private channel...", colour=discord.Color.dark_red()))
                        break

                    messages = messagess.split('/')
                    channels = self.bot.get_channel(int(messages[5]))
                    servers = self.bot.get_guild(int(messages[4]))
                    if not servers:
                        await message.channel.send(embed=discord.Embed(description=f"Hey,{message.author.mention}\nI can't chase that message...\nI haven't join to that server...", colour=discord.Color.dark_red()))
                        break

                    try:
                        if "\n" in messages[6]:
                            message_id = messages[6].split('\n')[0]
                        elif messages[6].split():
                            message_id = messages[6].split()[0]
                        else:
                            message_id = messages[6]
                        msg = await channels.fetch_message(int(message_id))
                        link1 = re.findall("https?://discordapp.com/channels/[0-9]+/[0-9]+/[0-9]+", msg.content)
                        link2 = re.findall("https?://canary.discordapp.com/channels/[0-9]+/[0-9]+/[0-9]+", msg.content)
                        if link1:
                            messagess = f"{link1[0]}"
                        elif link2:
                            messagess = f"{link2[0]}"
                        else:
                            author = msg.author
                            content = msg.content
                            guild_name = msg.guild.name
                            channel_name = msg.channel.name

                            if msg.embeds and msg.embeds[0]:
                                embed = discord.Embed(description=f"[Message URL](<https://discordapp.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}>)", timestamp=msg.created_at)
                                embed.set_author(name=f"Guild: [{guild_name}] | Channel: [{channel_name}]", icon_url=msg.guild.icon_url)
                                embed.set_footer(text=f"Author: [{author}]", icon_url=author.avatar_url)
                                if msg.reactions:
                                    embed.add_field(name="Reaction:", value=", ".join([f":{e.emoji}:`{e.count}`" for e in msg.reactions]))
                                await message.channel.send(embed=embed)
                                if content:
                                    await message.channel.send(content=content, embed=msg.embeds[0])
                                    break

                                else:
                                    await message.channel.send(embed=msg.embeds[0])
                                    break

                            if any([True for s in ['.jpg', '.png', '.jpeg', '.tif', '.tiff', '.bmp', '.gif', '.mp4'] if s in content]):
                                embed = discord.Embed(timestamp=msg.created_at)
                                embed.set_image(url=content)

                            elif msg.attachments and content:
                                embed = discord.Embed(description=f"{content}\n\n[Message URL](<https://discordapp.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}>)", timestamp=msg.created_at)
                                embed.set_image(url=msg.attachments[0].url)
                            elif msg.attachments:
                                embed = discord.Embed(timestamp=msg.created_at)
                                embed.set_image(url=msg.attachments[0].url)
                            else:
                                embed = discord.Embed(description=f"{content}\n\n[Message URL](<https://discordapp.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}>)", timestamp=msg.created_at)
                            if msg.reactions:
                                embed.add_field(name="Reaction:", value=", ".join([f":{e.emoji}:`{e.count}`" for e in msg.reactions]))
                            embed.set_author(name=f"Guild: [{guild_name}] | Channel: [{channel_name}]", icon_url=msg.guild.icon_url)
                            embed.set_footer(text=f"Author: [{author}]", icon_url=author.avatar_url)
                            await message.channel.send(embed=embed)
                            break

                    except discord.errors.Forbidden:
                        await message.author.send(embed=discord.Embed(description=f"Hey,{message.author.mention}\nI can't that channel message...\nI think I don't have permission to chase that message...", colour=discord.Color.dark_red()))
                        break

                    except discord.errors.NotFound:
                        await message.author.send(embed=discord.Embed(description=f"Hey,{message.author.mention}\nI can't that channel message...\nI think This message does not existed...", colour=discord.Color.dark_red()))
                        break


def setup(bot):
    bot.add_cog(Help(bot))
