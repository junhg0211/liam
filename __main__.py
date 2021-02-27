from os import listdir, environ
from sys import argv

from discord import Intents
from discord.ext import commands

from const import const

client = commands.Bot(const['command-prefix'], intent=Intents.all(), help_command=None)

for file_name in listdir('./cogs'):
    if file_name.endswith('.py'):
        client.load_extension(f'cogs.{file_name[:-3]}')
        print(f'`{file_name}` Cog가 준비되었습니다.')

if len(argv) >= 2:
    client.run(argv[1])
else:
    client.run(environ['BOT_TOKEN'])
