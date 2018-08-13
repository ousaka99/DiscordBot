import random
from collections import defaultdict


class BotCommand:
    def __init__(self, logger, config, json_data):
        self.logger = logger
        self.config = config
        self.json_data = json_data
        self.commands_comment = dict()
        self.commands_comment[self.config.command_help] = ""
        self.commands_comment[self.config.command_tier] = " 最小Tier 最大Tier"
        self.commands_comment[self.config.command_ship] = (" 最小Tier 最大Tier "
                                                           "(リクエスト回数やBB、CA、DD、日、米指定など)")
        self.commands_comment[self.config.command_choice] = " 選択肢1 (選択肢2 選択肢3...)"
        self.commands_comment[self.config.command_pickup] = " 選択数 選択肢1 (選択肢2 選択肢3...)"
        self.commands_comment[self.config.command_team] = " チーム数 選択肢1 選択肢2 (選択肢3 選択肢4...)"
        kinds = set()
        for x in self.json_data.luck_data["luck_comment"]:
            kinds.add(x)
        self.commands_comment[self.config.command_luck] = " (" + "、".join(kinds) + ")"

    def bot_command_help(self, words):
        params = words[1:]
        options = params[0:]
        comment = "使用できるコマンドは"
        comments = []

        for option in options:
            if option.startswith("-c"):
                comment = option[2:]

        for x in self.config.release_commands:
            comments.append(f"{x}{self.commands_comment[x]}")

        msg = f'{comment}\n'
        msg += ('\n'.join(comments) + '\nです。'
                '各コマンドには-cオプションがあり、見出しが設定できます。例)!luck -c明日の運勢は\n')
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
            msg = (f'すみません。よく分かりませんでした。'
                   f'```'
                   f'例）{self.config.command_tier}{self.commands_comment[self.config.command_tier]}'
                   f'```')
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
            msg = (f'すみません。よく分かりませんでした。'
                   f'```'
                   f'例）{self.config.command_ship}{self.commands_comment[self.config.command_ship]}'
                   f'```')
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
            ship_data = self.json_data.ship_data

            target_ship_data = [x for x in ship_data['ships'] if min_tier <= int(x['tier']) <= max_tier]
            if len(kinds) > 0:
                target_ship_data = [x for x in target_ship_data if x['kind'] in kinds]
            if len(nations) > 0:
                target_ship_data = [x for x in target_ship_data if x['nation'] in nations]

            if len(target_ship_data) < 1:
                ships = []
            else:
                ships = []
                if len(target_ship_data) < request_count:
                    request_count = len(target_ship_data)
                samples = random.sample(target_ship_data, request_count)
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
            msg = (f'すみません。よく分かりませんでした。'
                   f'```'
                   f'例）{self.config.command_choice}{self.commands_comment[self.config.command_choice]}'
                   f'```')
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
            msg = (f'すみません。よく分かりませんでした。'
                   f'```'
                   f'例）{self.config.command_pickup}{self.commands_comment[self.config.command_pickup]}'
                   f'```')
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

    def bot_command_team(self, words):
        result = self.bot_command_team_execute(words)
        teams = result[0]
        comment = result[1]

        msg = ''
        if teams is not None:
            if len(comment) > 0:
                msg = f"{comment}"

            for x in teams.keys():
                team_idx = x + 1
                msg += f"\n■Team{team_idx}が\n"
                msg += '\n'.join(teams[x])

            msg += '\nでいいと思います。'
        else:
            msg = (f'すみません。よく分かりませんでした。'
                   f'```'
                   f'例）{self.config.command_team}{self.commands_comment[self.config.command_team]}'
                   f'```')
        return msg

    def bot_command_team_execute(self, words):
        params = words[1:]
        options = params[1:]
        team_count = -1
        choices = []
        teams = defaultdict(list)
        comment = "チーム分けは"
        if len(params) >= 1:
            try:
                team_count = int(params[0])
            except ValueError:
                # PythonにはTryParseが無いため、実際にキャストしてみる(エラーは握り潰し)
                pass

        for option in options:
            if option.startswith("-c"):
                comment = option[2:]
            else:
                choices.append(option)

        self.logger.debug(f'pickup_count={team_count},'
                          f'choices={choices},'
                          f'comment={comment}')

        if 0 < team_count <= len(choices):
            random.shuffle(choices)
            for i, choice in enumerate(choices):
                team_idx = i % team_count
                teams[team_idx].append(choice)
        else:
            teams = None

        return teams, comment

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
        kinds = set()
        kind = "くじ"
        comment = ""

        for x in self.json_data.luck_data["luck_comment"]:
            kinds.add(x)

        for option in options:
            if option.startswith("-c"):
                comment = option[2:]
            elif option in kinds:
                kind = option

        if comment == "":
            comment = self.json_data.luck_data["luck_comment"][kind]

        items = self.json_data.luck_data["luck_items"][kind]

        for item in items:
            for n in range(0, int(item[1])):
                choices.append(item[0])

        self.logger.debug(f'choices={choices},'
                          f'comment={comment}')
        choice = random.choice(choices)
        return choice, comment

    def bot_command_kuji(self, words):
        result = self.bot_command_kuji_execute(words)
        choice = result[0]
        comment = result[1]

        msg = ''
        if len(comment) > 0:
            msg = f"{comment}\n"
        msg += f'{choice} です。'

        return msg

    def bot_command_kuji_execute(self, words):
        params = words[1:]
        choices = []
        comment = ""

        # TODO 未実装
        choice = ""
        return choice, comment
