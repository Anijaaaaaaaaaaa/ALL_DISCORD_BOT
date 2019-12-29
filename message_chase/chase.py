import json
import discord
import asyncio
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
        try:
            self.load_extension('cogs.help')
        except commands.errors.ExtensionAlreadyLoaded:
            pass
        await self.change_presence(activity=discord.Game(name="mc!help"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
