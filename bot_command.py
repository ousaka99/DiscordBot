import json
import random


class BotCommand:
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        pass

    def bot_command_help(self, words):
        msg = f'使用できるコマンドは\n'
        msg += '\n'.join(self.config.commands) + '\nです。'
        return msg

    def bot_command_tier(self, words):
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

        self.logger.debug(f'min_tier={min_tier},max_tier={max_tier},comment={comment}')
        if (1 <= min_tier <= 10) and (1 <= max_tier <= 10) and min_tier <= max_tier:
            tiers = list(range(min_tier, max_tier + 1))
            tier = random.choice(tiers)
            msg = ''
            if len(comment) > 0:
                msg = f"{comment}\n"
            msg += f'Tier{tier} がいいと思います。'
            return msg
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                  f'```' + \
                  f'例）{self.config.command_tier}<半角スペース>最小Tier<半角スペース>最大Tier' + \
                  f'```'
            return msg

    def bot_command_ship(self, words):
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

        self.logger.debug(f'min_tier={min_tier},max_tier={max_tier},request_count={request_count},kinds={kinds},comment={comment}')
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

            if len(kinds) > 0:
                # 艦種指定あり
                target_table_data = [x for x in table_data['ships'] if min_tier <= int(x['tier']) <= max_tier and x['kind'] in kinds]
            else:
                target_table_data = [x for x in table_data['ships'] if min_tier <= int(x['tier']) <= max_tier]

            if len(target_table_data) < 1:
                msg = f'すみません。おすすめを見つけることができませんでした。'
                return msg
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
                msg += '\n'.join(ships) + '\nがいいと思います。'
                return msg
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{self.config.command_ship}<半角スペース>最小Tier<半角スペース>最大Tier(<半角スペース>リクエスト回数やCV、BB、CA、DD指定など)' + \
                f'```'
            return msg

    def bot_command_choice(self, words):
        params = words[1:]
        options = params[0:]
        choices = []
        comment = ""

        for option in options:
            if option.startswith("-c"):
                comment = option[2:]
            else:
                choices.append(option)

        self.logger.debug(f'choices={choices},comment={comment}')
        if len(choices) >= 1:
            choice = random.choice(choices)
            msg = ''
            if len(comment) > 0:
                msg = f"{comment}\n"
            msg += f'{choice} がいいと思います。'
            return msg
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{self.config.command_choice}<半角スペース>選択肢1(<半角スペース>選択肢2<半角スペース>選択肢3...)' + \
                f'```'
            return msg

    def bot_command_pickup(self, words):
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

        self.logger.debug(f'pickup_count={pickup_count},choices={choices},comment={comment}')
        if 0 < pickup_count <= len(choices):
            pickups = random.sample(choices, pickup_count)
            msg = ''
            if len(comment) > 0:
                msg = f"{comment}\n"
            msg += '\n'.join(pickups) + '\nがいいと思います。'
            return msg
        else:
            msg = f'すみません。よく分かりませんでした。' + \
                f'```' + \
                f'例）{self.config.command_pickup}<半角スペース>選択数<半角スペース>選択肢1(<半角スペース>選択肢2<半角スペース>選択肢3...)' + \
                f'```'
            return msg

    def bot_command_luck(self, words):
        result = self.bot_command_luck_choice(words)
        choice = result[0]
        comment = result[1]

        msg = ''
        if len(comment) > 0:
            msg = f"{comment}\n"
        msg += f'{choice} です。'

        return msg

    def bot_command_luck_choice(self, words):
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

        self.logger.debug(f'choices={choices},comment={comment}')
        choice = random.choice(choices)
        return choice, comment
