import bot_command
import bot_config
import bot_json_data
import discord
import logging.config
import recruit_command

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
    global command, recruit
    command = bot_command.BotCommand(logger, config, json_data)
    recruit = recruit_command.RecruitCommand(logger, config)
    print('load json data')
    print('-----')


@client.event
async def on_message(message):
    if (message.author == client.user):
        # 自分自身の発言は無視する。
        return

    if (message.channel.id not in config.all_channel_ids):
        # 登録されていないチャンネルの発言は無視する。
        return

    translated_message = message.content
    for s in config.command_forward_match:
        if translated_message.startswith(s):
            translated_message = s + " " + translated_message[len(s):]
            break

    words = translated_message.split()
    if (words[0] not in config.release_commands):
        # 登録されているコマンド以外は無視する。
        return

    logger.info(message.content)

    if message.author.voice_channel is None:
        voice_channel_name = 'None'
    else:
        voice_channel_name = message.author.voice_channel.name#

    return_message = ''

    # 表示名称の取得
    if message.author.nick is None:
        display_name = message.author.name
    else:
        display_name = message.author.nick

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
    elif any(map(message.content.startswith, config.command_recruit_open)):
        if (message.channel.id in config.recruit_channel_ids):
            return_message = recruit.bot_command_recruit_open(words, message, display_name)
    elif any(map(message.content.startswith, config.command_recruit_close)):
        if (message.channel.id in config.recruit_channel_ids):
            return_message = recruit.bot_command_recruit_close(words, message, display_name)
    elif any(map(message.content.startswith, config.command_recruit_regist)):
        if (message.channel.id in config.recruit_channel_ids):
            return_data = []
            return_data = recruit.bot_command_recruit_regist(words, message, display_name)
            return_message = return_data[0]
            return_flag = return_data[1]
            notify_role = discord.utils.get(message.author.server.roles, id=config.recruit_role_id)
            if return_flag == 'ON':
                await client.add_roles(message.author, notify_role)
            elif return_flag == 'OFF':
                await client.remove_roles(message.author, notify_role)
    else:
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
