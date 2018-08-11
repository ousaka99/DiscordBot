import bot_command
import bot_config
import discord
import logging.config
import random

# <editor-fold desc="setting">
logging.config.fileConfig("logging.conf")
logger = logging.getLogger()
config = bot_config.BotConfig()
command = bot_command.BotCommand(logger, config)
client = discord.Client()
commandUsers = []
# </editor-fold>


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
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

    global commandUsers
    if len(commandUsers) > 2:
        commandUsers.pop(0)

    if (message.channel.id not in config.special_channel_ids) and (message.author.voice_channel is None):
        if message.author not in commandUsers:
            if 0 == random.choice(range(2)):
                msg = f'すみません。今気づきました。続けてもう一度お願いします。ボイスチャンネルに入っていただけるとすぐ気づくのですが、、、'
                commandUsers.append(message.author)
                await client.send_message(message.channel, msg)
                return
        elif 0 == random.choice(range(4)):
            msg = f'すみません。よく聞き取れませんでした。続けてもう一度お願いします。'
            commandUsers.append(message.author)
            await client.send_message(message.channel, msg)
            return

    if (message.channel.id not in config.special_channel_ids) and (message.author.voice_channel is None):
        voice_channel_name = 'ボイスチャンネル未接続(聞き取れないことがあります)'
    elif message.author.voice_channel is None:
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
    elif message.content.startswith(config.command_luck):
        return_message = command.bot_command_luck(words)

    return_message += f'from {voice_channel_name}'
    if len(return_message) > 2000:
        return_message = f'すみません。少し長すぎます。短くしてください。'

    await client.send_message(message.channel, return_message)

client.run(config.bot_token)
