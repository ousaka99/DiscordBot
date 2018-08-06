import configparser
import discord
import random
import json

# setting
config = configparser.ConfigParser()
config.read('./setting.conf', encoding="utf-8_sig")
config_bot_token = config['default']['bot_token']
config_channel_ids = config['default']['channel_id'].split()
config_command_tier = config['default']['command_tier']
config_command_ship = config['default']['command_ship']
config_command_choice = config['default']['command_choice']
config_command_pickup = config['default']['command_pickup']
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')


@client.event
async def on_message(message):
    if (message.author == client.user) or (message.channel.id not in config_channel_ids):
        return

    if message.content.startswith(config_command_tier):
        if message.author.voice_channel is None:
            msg = f'すみません。{config_command_tier}はボイスチャンネルに入っている人しか使えないコマンドです。'
            await client.send_message(message.channel, msg)
            return

        params = message.content.split()
        min_tier = -1
        max_tier = -1
        if len(params) >= 3:
            try:
                min_tier = int(params[1])
                max_tier = int(params[2])
            except ValueError:
                # PythonにはTryParseが無いため、実際にキャストしてみる(エラーは握り潰し)
                pass

        if (1 <= min_tier <= 10) and (1 <= max_tier <= 10) and min_tier <= max_tier:
            tiers = list(range(min_tier, max_tier + 1))
            tier = random.choice(tiers)
            msg = f'Tier{tier} がいいと思います。\n' + \
                f'from {message.author.voice_channel.name}'
            await client.send_message(message.channel, msg)
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{config_command_tier}<半角スペース>最小Tier<半角スペース>最大Tier' + \
                f'```'
            await client.send_message(message.channel, msg)
            return

    elif message.content.startswith(config_command_ship):
        if message.author.voice_channel is None:
            msg = f'すみません。{config_command_ship}はボイスチャンネルに入っている人しか使えないコマンドです。'
            await client.send_message(message.channel, msg)
            return

        params = message.content.split()
        min_tier = -1
        max_tier = -1
        request_count = 1
        kinds = []
        if len(params) >= 3:
            try:
                min_tier = int(params[1])
                max_tier = int(params[2])
            except ValueError:
                # PythonにはTryParseが無いため、実際にキャストしてみる(エラーは握り潰し)
                pass

        if len(params) >= 4:
            options = params[3:]

            for option in options:
                try:
                    request_count = int(option)
                except ValueError:
                    # PythonにはTryParseが無いため、実際にキャストしてみる(エラーは握り潰し)
                    pass

            for option in options:
                if 'CV' in option:
                    kinds.append('空母')
                if 'BB' in option:
                    kinds.append('戦艦')
                if 'CA' in option:
                    kinds.append('巡洋')
                if 'DD' in option:
                    kinds.append('駆逐')

        if request_count > 20:
            msg = f'すみません。欲張りすぎです。もうちょっと少なくしてください。'
            await client.send_message(message.channel, msg)
            return

        if (1 <= min_tier <= 10) and (1 <= max_tier <= 10) and min_tier <= max_tier and 0 < request_count:
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
                await client.send_message(message.channel, msg)
                return

            ships = []
            if len(target_table_data) < request_count:
                request_count = len(target_table_data)
            samples = random.sample(target_table_data, request_count)
            for x in samples:
                name = x['name']
                tier = x['tier']
                ships.append(f'{name}(Tier{tier})')

            msg = '\n'.join(ships) + '\nがいいと思います。' + \
                f'from {message.author.voice_channel.name}'
            await client.send_message(message.channel, msg)
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{config_command_ship}<半角スペース>最小Tier<半角スペース>最大Tier(<半角スペース>リクエスト回数やCV、BB、CA、DD指定など)' + \
                f'```'
            await client.send_message(message.channel, msg)
            return

    elif message.content.startswith(config_command_choice):
        if message.author.voice_channel is None:
            msg = f'すみません。{config_command_choice}はボイスチャンネルに入っている人しか使えないコマンドです。'
            await client.send_message(message.channel, msg)
            return

        params = message.content.split()
        if len(params) >= 2:
            choices = params[1:]

            choice = random.choice(choices)
            msg = f'{choice}がいいと思います。\n' + \
                  f'from {message.author.voice_channel.name}'
            await client.send_message(message.channel, msg)
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{config_command_choice}<半角スペース>選択肢1(<半角スペース>選択肢2<半角スペース>選択肢3...)' + \
                f'```'
            await client.send_message(message.channel, msg)
            return

    elif message.content.startswith(config_command_pickup):
        if message.author.voice_channel is None:
            msg = f'すみません。{config_command_pickup}はボイスチャンネルに入っている人しか使えないコマンドです。'
            await client.send_message(message.channel, msg)
            return

        params = message.content.split()
        pickup_count = -1
        if len(params) >= 2:
            try:
                pickup_count = int(params[1])
            except ValueError:
                # PythonにはTryParseが無いため、実際にキャストしてみる(エラーは握り潰し)
                pass

        if len(params) >= 3:
            choices = params[2:]

        if 0 < pickup_count <= len(choices):
            pickups = random.sample(choices, pickup_count)
            msg = '\n'.join(pickups) + '\nがいいと思います。' + \
                f'from {message.author.voice_channel.name}'
            await client.send_message(message.channel, msg)
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{config_command_pickup}<半角スペース>選択数<半角スペース>選択肢1(<半角スペース>選択肢2<半角スペース>選択肢3...)' + \
                f'```'
            await client.send_message(message.channel, msg)
            return

client.run(config_bot_token)
