import discord
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed

web_1 = "https://discordapp.com/api/webhooks/657882228662992899/0wyVXp1us11myWnltycXxudKnW5E14BmCjot7cxPyoi1G5soMxZ_JRwIiOhb9hVfBNPy"
web_2 = "https://discordapp.com/api/webhooks/657882313752838173/PP4t5A4SXkftc7qW6ikP3q75aZj1d0AwMV2re_b7hbPYy2BmMvgpKhm9WVzmhj9AcYIl"
web_3 = "https://discordapp.com/api/webhooks/657887491268935681/KBS143BMdp8ujLU4I2Ajtnm1TivZ2R6N9526Olrgmu83IaTsGXDFqNtkvDE945tFaETn"
web_4 = "https://discordapp.com/api/webhooks/657887580137717761/ZbCQKBRRLEYZJTS3qMqLc2-AI7UZO6EyCYvO79Q5jW_gMJZdgPiBh4MuEw7zVyu6SD8m"
web_5 = "https://discordapp.com/api/webhooks/657887620243914755/e1RXC4imvy2Bl5jcy7Sz72B8MbxB9ds6pETihbMTi8Gytx29WKqIejModFh-Q1-_STit"
web_hook_channels_id = [657765832478294047, 657769986303066113, 657765855496503299, 657766087529725962, 657765944952619037]
web_hook_channels = [web_1, web_2, web_3, web_4, web_5]
check = []


class Webhook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.webhook_id:
            return
        
        if isinstance(message.channel, discord.DMChannel):
            if message.author != self.bot.user:
                return await message.channel.send(embed=discord.Embed(description=f"{message.author.mention}さん。\nこのBOTはDM対応外です...", color=0xC41415))
            
        if message.channel.id in web_hook_channels_id:
            user_img = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.author)
            count = 0
            for channel_id in web_hook_channels_id:
                if channel_id == message.channel.id:
                    url = web_hook_channels[count]
                    webhook = DiscordWebhook(url=url, content=message.content, username=f"{message.author}", avatar_url=user_img)
                    if message.attachments:
                        embed = DiscordEmbed()
                        embed.set_image(url=f"{message.attachments[0].url}")
                        webhook.add_embed(embed)
                    webhook.execute()
                else:
                    count += 1


def setup(bot):
    bot.add_cog(Webhook(bot))
