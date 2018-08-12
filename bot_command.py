import json
import random


class BotCommand:
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        pass

    def bot_command_help(self):
        msg = f'使用できるコマンドは\n'
        msg += '\n'.join(self.config.commands) + '\nです。'
        return msg

    def bot_command_tier(self, words):
        result = self.bot_command_tier_execute(words)
        tier = result[0]
        comment = result[1]

        msg = ''
        if tier is not None:
            if len(comment) > 0:
                msg = f"{comment}\n"
            msg += f'Tier{tier} がいいと思います。'
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                  f'例）{self.config.command_tier}<半角スペース>最小Tier<半角スペース>最大Tier' + \
                  f'```'
        return msg

    def bot_command_tier_execute(self, words):
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

        self.logger.debug(f'min_tier={min_tier},'
                          f'max_tier={max_tier},'
                          f'comment={comment}')
        if (1 <= min_tier <= 10) and (1 <= max_tier <= 10) and min_tier <= max_tier:
            tiers = list(range(min_tier, max_tier + 1))
            tier = random.choice(tiers)
        else:
            tier = None

        return tier, comment

    def bot_command_ship(self, words):
        result = self.bot_command_ship_execute(words)
        ships = result[0]
        comment = result[1]

        msg = ''
        if ships is not None:
            if len(ships) == 0:
                msg = f'すみません。おすすめを見つけることができませんでした。'
            elif len(comment) > 0:
                msg = f"{comment}\n"
            msg += '\n'.join(ships) + '\nがいいと思います。'
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{self.config.command_ship}<半角スペース>最小Tier<半角スペース>最大Tier(<半角スペース>リクエスト回数やCV、BB、CA、DD指定など)' + \
                f'```'
        return msg

    def bot_command_ship_execute(self, words):
        params = words[1:]
        min_tier = -1
        max_tier = -1
        options = []    # 変動
        request_count = 1
        kinds = set()
        nations = set()
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
                kinds.add('空母')
            if 'BB' in option:
                kinds.add('戦艦')
            if 'CA' in option:
                kinds.add('巡洋')
            if 'DD' in option:
                kinds.add('駆逐')
            if '日' in option:
                nations.add('日本')
            if '米' in option:
                nations.add('アメリカ')
            if 'ソ' in option:
                nations.add('ソ連')
            if '独' in option:
                nations.add('ドイツ')
            if '英' in option:
                nations.add('イギリス')
            if '仏' in option:
                nations.add('フランス')
            if 'パ' in option:
                nations.add('パンジア')
            if '伊' in option:
                nations.add('イタリア')
            if '波' in option:
                nations.add('ポーランド')
            if 'イ' in option:
                nations.add('イギリス連邦')
            if 'ア' in option:
                nations.add('パンアメリカ')

        self.logger.debug(f'min_tier={min_tier},'
                          f'max_tier={max_tier},'
                          f'request_count={request_count},'
                          f'kinds={kinds},'
                          f'nations={nations},'
                          f'comment={comment}')
        if request_count > 20:
            msg = f'すみません。欲張りすぎです。もうちょっと少なくしてください。'
            return msg
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

            target_table_data = [x for x in table_data['ships'] if min_tier <= int(x['tier']) <= max_tier]
            if len(kinds) > 0:
                target_table_data = [x for x in target_table_data if x['kind'] in kinds]
            if len(nations) > 0:
                target_table_data = [x for x in target_table_data if x['nation'] in nations]

            if len(target_table_data) < 1:
                ships = []
            else:
                ships = []
                if len(target_table_data) < request_count:
                    request_count = len(target_table_data)
                samples = random.sample(target_table_data, request_count)
                for x in samples:
                    name = x['name']
                    tier = x['tier']
                    ships.append(f'{name}(Tier{tier})')
        else:
            ships = None

        return ships, comment

    def bot_command_choice(self, words):
        result = self.bot_command_choice_execute(words)
        choice = result[0]
        comment = result[1]

        msg = ''
        if choice is not None:
            if len(comment) > 0:
                msg = f"{comment}\n"
            msg += f'{choice} がいいと思います。'
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{self.config.command_choice}<半角スペース>選択肢1(<半角スペース>選択肢2<半角スペース>選択肢3...)' + \
                f'```'
        return msg

    def bot_command_choice_execute(self, words):
        params = words[1:]
        options = params[0:]
        choices = []
        comment = ""

        for option in options:
            if option.startswith("-c"):
                comment = option[2:]
            else:
                choices.append(option)

        self.logger.debug(f'choices={choices},'
                          f'comment={comment}')

        if len(choices) >= 1:
            choice = random.choice(choices)
        else:
            choice = None

        return choice, comment

    def bot_command_pickup(self, words):
        result = self.bot_command_pickup_execute(words)
        pickups = result[0]
        comment = result[1]

        msg = ''
        if pickups is not None:
            if len(comment) > 0:
                msg = f"{comment}\n"
            msg += '\n'.join(pickups) + '\nがいいと思います。'
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{self.config.command_pickup}<半角スペース>選択数<半角スペース>選択肢1(<半角スペース>選択肢2<半角スペース>選択肢3...)' + \
                f'```'
        return msg

    def bot_command_pickup_execute(self, words):
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

        self.logger.debug(f'pickup_count={pickup_count},'
                          f'choices={choices},'
                          f'comment={comment}')
        if 0 < pickup_count <= len(choices):
            pickups = random.sample(choices, pickup_count)
        else:
            pickups = None
        return pickups, comment

    def bot_command_luck(self, words):
        result = self.bot_command_luck_execute(words)
        choice = result[0]
        comment = result[1]

        msg = ''
        if len(comment) > 0:
            msg = f"{comment}\n"
        msg += f'{choice} です。'

        return msg

    def bot_command_luck_execute(self, words):
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

        self.logger.debug(f'choices={choices},'
                          f'comment={comment}')
        choice = random.choice(choices)
        return choice, comment
