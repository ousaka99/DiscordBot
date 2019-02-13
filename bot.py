import bot_command
import bot_config
import bot_json_data
import discord
import logging.config
import random

# <editor-fold desc="setting">
logging.config.fileConfig("logging.conf")
logger = logging.getLogger()
config = bot_config.BotConfig()
json_data = bot_json_data.BotJsonData(logger, config)
command = None
client = discord.Client()
authors = []
# </editor-fold>


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')
    json_data.bot_json_data()
    global command
    command = bot_command.BotCommand(logger, config, json_data)
    print('load json data')
    print('-----')


@client.event
async def on_message(message):
    if (message.author == client.user) or (message.channel.id not in config.all_channel_ids):
        # 自分自身の発言や、登録されていないチャンネルの発言は無視する。
        return

    words = message.content.split()
    if words[0] not in config.commands:
        # 登録されているコマンド以外は無視する。
        return

    logger.info(message.content)

    if message.author.voice_channel is None:
        voice_channel_name = 'None'
    else:
        voice_channel_name = message.author.voice_channel.name

    return_message = ""

    if message.content.startswith(config.command_help):
        return_message = command.bot_command_help(words)
    elif message.content.startswith(config.command_tier):
        return_message = command.bot_command_tier(words)
    elif message.content.startswith(config.command_ship):
        return_message = command.bot_command_ship(words)
    elif message.content.startswith(config.command_choice):
        return_message = command.bot_command_choice(words)
    elif message.content.startswith(config.command_pickup):
        return_message = command.bot_command_pickup(words)
    elif message.content.startswith(config.command_team):
        return_message = command.bot_command_team(words)
    elif message.content.startswith(config.command_luck):
        return_message = command.bot_command_luck(words)
    elif message.content.startswith(config.command_kuji):
        return_message = command.bot_command_kuji(words)
    elif message.content.startswith(config.command_enter):
        # TODO 未実装
        pass
    elif message.content.startswith(config.command_leave):
        # TODO 未実装
        pass

    if words[0] in config.release_commands:
        return_message += f'from {voice_channel_name}'
        if len(return_message) > 2000:
            return_message = f'すみません。少し長すぎます。短くしてください。'

        await client.send_message(message.channel, return_message)

try:
    client.run(config.bot_token)
except Exception as e:
    logger.error(f'client.run Error:{e}')
    exit(e)
finally:
    logger.info(f'client.run end')
