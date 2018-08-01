import configparser
import discord
import random

# setting
config = configparser.ConfigParser()
config.read('./setting.conf', encoding="utf-8_sig")
config_bot_token = config['default']['bot_token']
config_channel_ids = config['default']['channel_id'].split()
config_command_tier = config['default']['command_tier']
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

    # Tier選択コマンド
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
                print(f'message={message.content}')

        if (1 <= min_tier <= 10) and (1 <= max_tier <= 10) and min_tier <= max_tier:
            tiers = list(range(min_tier, max_tier + 1))
            tier = random.choice(tiers)
            msg = f'Tier{tier} がいいと思います。\n' + \
                f'from {message.author}@{message.author.voice_channel.name}'
            await client.send_message(message.channel, msg)
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{config_command_tier}<半角スペース>最小Tier<半角スペース>最大Tier' + \
                f'```'
            await client.send_message(message.channel, msg)

    # for server in client.servers:
    #     for channel in server.channels:
    #         # print(f'channel type={channel.type}, name={channel.name}, id={channel.id}')
    #         if channel.type == discord.ChannelType.voice:
    #             for member in channel.voice_members:
    #                 print(f'voice channel={channel.name}, member={member}')

client.run(config_bot_token)
