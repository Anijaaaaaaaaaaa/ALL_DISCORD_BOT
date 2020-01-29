import json
import discord
import traceback
import asyncio
from discord.ext import commands

loop = asyncio.new_event_loop()
with open(r'setting.json', mode='r', encoding='utf-8') as fh:
    json_txt = fh.read()
    json_txt = str(json_txt).replace("'", '"').replace('True', 'true').replace('False', 'false')
    token = json.loads(json_txt)['token']
    prefix = json.loads(json_txt)['prefix']


async def run():
    try:
        bot = MyBot()
        try:
            await bot.start(token)
        except KeyboardInterrupt:
            await bot.logout()
            await bot.close()
            await bot.clear()

    except Exception as _:
        print("エラー情報\n" + traceback.format_exc())


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(prefix), loop=loop)
        self.remove_command('help')

    async def on_ready(self):
        try:
            self.load_extension('cogs.help')
        except commands.errors.ExtensionAlreadyLoaded:
            pass

        await self.change_presence(activity=discord.Game(name=f"{prefix}help | {len(self.guilds)}guilds", type=1))

    async def on_command_error(self, ctx, error1):
        if isinstance(error1, (commands.CommandNotFound, commands.CommandInvokeError, commands.BadArgument, commands.UnexpectedQuoteError, commands.CommandOnCooldown, commands.MissingPermissions, commands.MissingRequiredArgument)):
            return

        elif isinstance(error1, commands.BotMissingPermissions):
            permission = {'read_messages': "read_messages", 'send_messages': "send_messages", 'read_message_history': "read_message_history", 'embed_links': "embed_links"}
            text = ""
            for all_error_permission in error1.missing_perms:
                text += f"❌:{permission[all_error_permission]}\n"
                del permission[all_error_permission]

            for all_arrow_permission in list(permission.values()):
                text += f"✅:{all_arrow_permission}\n"

            embed = discord.Embed(description=text)
            return await ctx.message.author.send(embed=embed)
        else:
            print("エラー情報\n" + traceback.format_exc())
    
    async def on_guild_join(self, _):
        await self.change_presence(activity=discord.Game(name=f"{prefix}help | {len(self.guilds)}guilds", type=1))
    
    async def on_guild_remove(self, _):
        await self.change_presence(activity=discord.Game(name=f"{prefix}help | {len(self.guilds)}guilds", type=1))


if __name__ == '__main__':
    try:
        print("ready!")
        main_task = loop.create_task(run())
        loop.run_until_complete(main_task)
        loop.close()

    except Exception as error:
        print("エラー情報\n" + traceback.format_exc())
