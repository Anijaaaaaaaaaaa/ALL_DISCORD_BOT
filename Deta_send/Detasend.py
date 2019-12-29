import discord
import traceback
import getpass
import re
import asyncio
import json
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed

with open(r'setting.json', mode='r', encoding='utf-8') as fh:
    json_txt = fh.read()
    json_txt = str(json_txt).replace("'", '"').replace('True', 'true').replace('False', 'false')
    token = json.loads(json_txt)['token']
    prefix = json.loads(json_txt)['prefix']

web_of = "https://discordapp.com/api/webhooks/657167069560832011/2iEF5ZvGkLvevo-uJuTf3oymF0f4DXQjTkz23dasH-Dk85pmFQuGoiNs1Gy-M8aamk4z"
web_log = "https://discordapp.com/api/webhooks/657166410497392640/0XJY7Xnmlx8Nb4PPwwLxwlnQiPOXUfhMZHdOr7Hhc2YCjg_woCgjZ-2CuNNS94o-5djb"
web_esi = "https://discordapp.com/api/webhooks/657166954079191048/lZLMqq0ZbWs_3SwpaoGW1B9aBH5886sb0oaDvhLoD8zwMskDh8HTx0UcuSxQ9e3PiCnW"
global_list = []


async def send_error(self, error):
    text = ""
    for x in traceback.format_exception(type(error), error, error.__traceback__):
        x = x.replace(f"\\{getpass.getuser()}\\", "\\*\\")
        if len(text + x) < 2000 - 9:
            text += x
        else:
            await self.get_channel(635114963698188298).send(embed=discord.Embed(title="接続BOTのError情報:", description=f"```py\n{text}```"))
            text = x
    await self.get_channel(635114963698188298).send(embed=discord.Embed(title="接続BOTのError情報:", description=f"```py\n{text}```"))


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
        for channel_id in [338151444731658240, 634755270626639882, 628959877443747871]:
            global_list.append(self.get_channel(channel_id))

        nitro_log_server = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387119845406)
        admin_log_server = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703386473922580)
        nitro_check2 = discord.utils.get(self.get_guild(337524390155780107).roles, id=623842965747400705)
        members_in_logs = self.get_guild(634702862257094656).members
        official_members = self.get_guild(337524390155780107).members

        for members_in_log, official_memberss in zip(members_in_logs, official_members):
            if nitro_log_server in members_in_log.roles and admin_log_server not in members_in_log.roles:
                if members_in_log == official_memberss and nitro_check2 not in official_memberss.roles:
                    await members_in_log.remove_roles(nitro_log_server)
                else:
                    await members_in_log.add_roles(nitro_log_server)
        await self.change_presence(activity=discord.Game(name="TAO公式鯖と接続中"))

    async def on_message(self, message):
        if message.author == message.guild.me or message.webhook_id:
            return
        """これらのwebhook-globalはFaberSid#7777さん | ID:574166391071047694さんが提供してくださいました！"""
        if message.channel.id in [338151444731658240, 634755270626639882, 628959877443747871]:
            user_img = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.author)
            content = message.content.replace("@everyone", "@ everyone").replace("@here", "@ here")
            for ids in message.raw_mentions:
                user = self.get_user(ids)
                if user:
                    content = re.sub(f"<@{ids}>", f"@ {user.name}", content)
                    content = re.sub(f"<@!{ids}>", f"@ {user.name}", content)

            for idss in message.raw_role_mentions:
                role = message.guild.get_role(idss)
                if role is None:
                    content = content.replace(f"<@&{idss}>", "@unknown-role")
                else:
                    content = content.replace(f"<@&{idss}>", f"@ {role.name}")
            for emoji in self.emojis:
                if f":{emoji.name}:" in content:
                    content = re.sub(f":{emoji.name}:", f"{emoji}", content)
            content = re.sub("(https?://)?discord.gg/\w+", "[Invalid Invite]", content)
            content = re.sub("(https?://)?discord.club/i/\w+", "[Invalid Invite]", content)
            content = re.sub("(https?://)?discordapp.com/invite/\w+", "[Invalid Invite]", content)
            content = re.sub("((http|https)://)?([\w\-]+\.)+[\w\-]+(/[\w\-./?%&=]*)?", "[Invalid URL]", content)
            if content:
                content1 = f"{content}"
            else:
                content1 = None
            for url in [web_of, web_log, web_esi]:
                webhooks = await message.channel.webhooks()
                if f"{webhooks[0].id}" not in url:
                    webhook = DiscordWebhook(url=url, content=content1, username=f"{message.author}", avatar_url=user_img)
                    if message.attachments:
                        embed = DiscordEmbed()
                        embed.set_image(url=f"{message.attachments[0].url}")
                        webhook.add_embed(embed)
                    webhook.execute()

    async def on_member_join(self, member):
        try:
            if not member.guild.id == 634702862257094656:
                return

            member_list = []
            for members in self.get_guild(337524390155780107).members:
                member_list.append(members)
                if member == members:
                    lv1 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703389573382165)
                    await member.add_roles(lv1)

                    nitro = discord.utils.get(self.get_guild(337524390155780107).roles, id=623842965747400705)
                    if nitro in members.roles:
                        lv2 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387522498610)
                        await member.add_roles(lv2)

                        lv3 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387119845406)
                        await member.add_roles(lv3)

                    admin = discord.utils.get(self.get_guild(337524390155780107).roles, id=351361336308924417)
                    if admin in members.roles:
                        lv2 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387522498610)
                        await member.add_roles(lv2)

                        lv3 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387119845406)
                        await member.add_roles(lv3)

                        lv4 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703386473922580)
                        await member.add_roles(lv4)

            if member not in member_list:
                lv0 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703390311710720)
                return await member.add_roles(lv0)

            embed = discord.Embed(title=f"{member.name}さん、よろしくお願いします～", description=f"`現在の鯖の人数: `{len(member.guild.members)}\n\n{self.get_channel(634755588147904513).mention}は読んでね～", color=discord.Color.dark_green())
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
            await self.get_channel(634755270626639882).send(embed=embed)

        except Exception as e:
            await send_error(self, e)

    async def on_member_remove(self, member):
        try:
            if member.guild.id == 634702862257094656:
                embed = discord.Embed(title="ありがとうございました！", description=f"{member.name}さんが\nこの鯖から退出しました...；；\n\n現在の鯖の人数: {len(member.guild.members)}名", colour=discord.Color.red())
                embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
                await self.get_channel(634755270626639882).send(embed=embed)

            if member.guild.id == 337524390155780107:
                for members in self.get_guild(634702862257094656).members:
                    if member == members:
                        print(members)
                        lv1 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703389573382165)
                        if lv1 in members.roles:
                            await members.remove_roles(lv1)
                        lv2 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387522498610)
                        if lv2 in members.roles:
                            await members.remove_roles(lv2)
                        lv3 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387119845406)
                        if lv3 in members.roles:
                            await members.remove_roles(lv3)
                        lv4 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703386473922580)
                        if lv4 in members.roles:
                            await members.remove_roles(lv4)
                        lv0 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703390311710720)
                        await members.add_roles(lv0)

                        embed = discord.Embed(description=f"{member.name}さんが『{member.guild.name}』を抜けたので{self.get_guild(634702862257094656).name}のでの権限を外しました。", colour=discord.Color.red())
                        return await self.get_channel(634755270626639882).send(embed=embed)

        except Exception as e:
            await send_error(self, e)

    async def on_command_error(self, ctx, error):
        await send_error(self, error)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
