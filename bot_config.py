import configparser


class BotConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./setting.conf', encoding="utf-8_sig")
        self.bot_token = self.config['default']['bot_token']
        self.channel_ids = self.config['default']['channel_id'].split()
        self.special_channel_ids = self.config['default']['special_channel_id'].split()
        self.recruit_channel_ids = self.config['default']['recruit_channel_id'].split()
        self.recruit_role_id = self.config['default']['recruit_role_id']
        self.all_channel_ids = []
        self.all_channel_ids.extend(self.channel_ids)
        self.all_channel_ids.extend(self.special_channel_ids)
        self.all_channel_ids.extend(self.recruit_channel_ids)
        self.command_prefix = self.config['default']['command_prefix']
        self.command_help = self.command_prefix + self.config['default']['command_help']
        self.command_tier = self.command_prefix + self.config['default']['command_tier']
        self.command_ship = self.command_prefix + self.config['default']['command_ship']
        self.command_choice = self.command_prefix + self.config['default']['command_choice']
        self.command_pickup = self.command_prefix + self.config['default']['command_pickup']
        self.command_team = self.command_prefix + self.config['default']['command_team']
        self.command_luck = self.command_prefix + self.config['default']['command_luck']
        self.command_kuji = self.command_prefix + self.config['default']['command_kuji']
        self.command_enter = self.command_prefix + self.config['default']['command_enter']
        self.command_leave = self.command_prefix + self.config['default']['command_leave']
        self.command_recruit_open = self.config['default']['command_recruit_open'].split()
        self.command_recruit_close = self.config['default']['command_recruit_close'].split()
        self.command_recruit_regist = self.config['default']['command_recruit_regist'].split()
        self.release_commands = [self.command_help,
                                 self.command_tier,
                                 self.command_ship,
                                 self.command_choice,
                                 self.command_pickup,
                                 self.command_team,
                                 self.command_luck]
        self.commands = list(self.release_commands)
        self.commands.append(self.command_kuji)
        self.commands.append(self.command_enter)
        self.commands.append(self.command_leave)
        self.commands.extend(self.command_recruit_open)
        self.commands.extend(self.command_recruit_close)
        self.commands.extend(self.command_recruit_regist)
