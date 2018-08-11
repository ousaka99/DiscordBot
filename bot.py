import configparser
import discord
import random
import json
import logging.config

# <editor-fold desc="setting">
config = configparser.ConfigParser()
config.read('./setting.conf', encoding="utf-8_sig")
config_bot_token = config['default']['bot_token']
config_channel_ids = config['default']['channel_id'].split()
config_command_help = config['default']['command_help']
config_command_tier = config['default']['command_tier']
config_command_ship = config['default']['command_ship']
config_command_choice = config['default']['command_choice']
config_command_pickup = config['default']['command_pickup']
config_command_uranai = config['default']['command_uranai']
commands = [config_command_help,
            config_command_tier,
            config_command_ship,
            config_command_choice,
            config_command_pickup,
            config_command_uranai]
client = discord.Client()
commandUsers = []
logging.config.fileConfig("logging.conf")
logger = logging.getLogger()
# </editor-fold>


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')


@client.event
async def on_message(message):
    if (message.author == client.user) or (message.channel.id not in config_channel_ids):
        # 自分自身の発言や、登録されていないチャンネルの発言は無視する。
        return

    words = message.content.split()
    if words[0] not in commands:
        # 登録されているコマンド以外は無視する。
        return

    logger.info(message.content)

    global commandUsers
    if message.author.voice_channel is None:
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

    if message.author.voice_channel is None:
        voice_channel_name = 'ボイスチャンネル未接続(聞き取れないことがあります)'
    else:
        voice_channel_name = message.author.voice_channel.name

    return_message = ""

    if message.content.startswith(config_command_help):
        msg = f'使用できるコマンドは\n'
        msg += '\n'.join(commands) + '\nです。' + \
               f'from {voice_channel_name}'

        return_message = msg

    elif message.content.startswith(config_command_tier):
        params = words[1:]
        min_tier = -1
        max_tier = -1
        options = params[2:]
        comment = ""
        if len(params) >= 2:
            try:
                min_tier = int(params[0])
                max_tier = int(params[1])
            except ValueError:
                # PythonにはTryParseが無いため、実際にキャストしてみる(エラーは握り潰し)
                pass
        for option in options:
            if option.startswith("-c"):
                comment = option[2:]

        logger.debug(f'min_tier={min_tier},max_tier={max_tier},comment={comment}')
        if (1 <= min_tier <= 10) and (1 <= max_tier <= 10) and min_tier <= max_tier:
            tiers = list(range(min_tier, max_tier + 1))
            tier = random.choice(tiers)
            msg = ''
            if len(comment) > 0:
                msg = f"{comment}\n"
            msg += f'Tier{tier} がいいと思います。' + \
                f'from {voice_channel_name}'
            return_message = msg
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{config_command_tier}<半角スペース>最小Tier<半角スペース>最大Tier' + \
                f'```'
            return_message = msg

    elif message.content.startswith(config_command_ship):
        params = words[1:]
        min_tier = -1
        max_tier = -1
        options = []    # 変動
        request_count = 1
        kinds = []
        comment = ""
        if len(params) >= 2:
            try:
                min_tier = int(params[0])
                max_tier = int(params[1])
            except ValueError:
                # PythonにはTryParseが無いため、実際にキャストしてみる(エラーは握り潰し)
                pass
        if len(params) >= 3:
            try:
                request_count = int(params[2])
            except ValueError:
                # PythonにはTryParseが無いため、実際にキャストしてみる(エラーは握り潰し)
                request_count = -1
            if request_count > 0:
                options = params[3:]
            else:
                request_count = 1
                options = params[2:]

        for option in options:
            if option.startswith("-c"):
                comment = option[2:]
            if 'CV' in option:
                kinds.append('空母')
            if 'BB' in option:
                kinds.append('戦艦')
            if 'CA' in option:
                kinds.append('巡洋')
            if 'DD' in option:
                kinds.append('駆逐')

        logger.debug(f'min_tier={min_tier},max_tier={max_tier},request_count={request_count},kinds={kinds},comment={comment}')
        if request_count > 20:
            msg = f'すみません。欲張りすぎです。もうちょっと少なくしてください。'
            return_message = msg
        elif (1 <= min_tier <= 10) and (1 <= max_tier <= 10) and min_tier <= max_tier and 0 < request_count:
            table_data = {}
            try:
                with open('./ship_table.json', 'r', encoding="utf-8_sig") as fc:
                    table_data = json.load(fc)
            except json.JSONDecodeError as e:
                print('JSONDecodeError: ', e)
                exit(e)
            except FileNotFoundError as e:
                print('FileNotFoundError: ', e)
                exit(e)

            if len(kinds) > 0:
                # 艦種指定あり
                target_table_data = [x for x in table_data['ships'] if min_tier <= int(x['tier']) <= max_tier and x['kind'] in kinds]
            else:
                target_table_data = [x for x in table_data['ships'] if min_tier <= int(x['tier']) <= max_tier]

            if len(target_table_data) < 1:
                msg = f'すみません。おすすめを見つけることができませんでした。'
                return_message = msg
            else:
                ships = []
                if len(target_table_data) < request_count:
                    request_count = len(target_table_data)
                samples = random.sample(target_table_data, request_count)
                for x in samples:
                    name = x['name']
                    tier = x['tier']
                    ships.append(f'{name}(Tier{tier})')
                msg = ''
                if len(comment) > 0:
                    msg = f"{comment}\n"
                msg += '\n'.join(ships) + '\nがいいと思います。' + \
                    f'from {voice_channel_name}'
                return_message = msg
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{config_command_ship}<半角スペース>最小Tier<半角スペース>最大Tier(<半角スペース>リクエスト回数やCV、BB、CA、DD指定など)' + \
                f'```'
            return_message = msg

    elif message.content.startswith(config_command_choice):
        params = words[1:]
        options = params[0:]
        choices = []
        comment = ""

        for option in options:
            if option.startswith("-c"):
                comment = option[2:]
            else:
                choices.append(option)

        logger.debug(f'choices={choices},comment={comment}')
        if len(choices) >= 1:
            choice = random.choice(choices)
            msg = ''
            if len(comment) > 0:
                msg = f"{comment}\n"
            msg += f'{choice} がいいと思います。' + \
                f'from {voice_channel_name}'
            return_message = msg
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{config_command_choice}<半角スペース>選択肢1(<半角スペース>選択肢2<半角スペース>選択肢3...)' + \
                f'```'
            return_message = msg

    elif message.content.startswith(config_command_pickup):
        params = words[1:]
        options = params[1:]
        pickup_count = -1
        choices = []
        comment = ""
        if len(params) >= 1:
            try:
                pickup_count = int(params[0])
            except ValueError:
                # PythonにはTryParseが無いため、実際にキャストしてみる(エラーは握り潰し)
                pass

        for option in options:
            if option.startswith("-c"):
                comment = option[2:]
            else:
                choices.append(option)

        logger.debug(f'pickup_count={pickup_count},kinds={kinds},comment={comment}')
        if 0 < pickup_count <= len(choices):
            pickups = random.sample(choices, pickup_count)
            msg = ''
            if len(comment) > 0:
                msg = f"{comment}\n"
            msg += '\n'.join(pickups) + '\nがいいと思います。' + \
                f'from {voice_channel_name}'
            return_message = msg
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{config_command_pickup}<半角スペース>選択数<半角スペース>選択肢1(<半角スペース>選択肢2<半角スペース>選択肢3...)' + \
                f'```'
            return_message = msg

    elif message.content.startswith(config_command_uranai):
        params = words[1:]
        options = params[0:]
        choices = []
        kind = ""
        comment = ""

        for option in options:
            if option.startswith("-c"):
                comment = option[2:]
            elif option == "色":
                kind = "色"

        if kind == "色":
            patterns = {'赤': 1,
                        'ピンク': 1,
                        '黄色': 1,
                        'オレンジ': 1,
                        '緑': 1,
                        '青': 1,
                        '紫': 1,
                        '茶色': 1,
                        '白': 1,
                        '黒': 1}
            if comment == "":
                comment = "今日のラッキーカラーは"
        else:
            patterns = {'大吉': 30,
                        '吉': 18,
                        '中吉': 14,
                        '小吉': 14,
                        '末吉': 16,
                        '凶': 8}
            if comment == "":
                comment = "今日の運勢は"

        for key in patterns.keys():
            for n in range(0, int(patterns[key])):
                choices.append(key)

        logger.debug(f'choices={choices},comment={comment}')
        choice = random.choice(choices)

        msg = ''
        if len(comment) > 0:
            msg = f"{comment}\n"
        msg += f'{choice} です。' + \
               f'from {voice_channel_name}'
        return_message = msg

    if len(return_message) > 2000:
        return_message = f'すみません。少し長すぎます。短くしてください。'

    await client.send_message(message.channel, return_message)

client.run(config_bot_token)
