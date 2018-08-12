import json


class BotJsonData:
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.ship_data = {}
        self.luck_data = {}

    def bot_json_data(self):
        self.ship_data = {}
        try:
            with open('./ship_table.json', 'r', encoding="utf-8_sig") as fc:
                self.ship_data = json.load(fc)
        except json.JSONDecodeError as e:
            self.logger.error(f'JSONDecodeError:{e}')
            exit(e)
        except FileNotFoundError as e:
            self.logger.error(f'FileNotFoundError:{e}')
            exit(e)

        self.luck_data = {}
        try:
            with open('./luck_table.json', 'r', encoding="utf-8_sig") as fc:
                self.luck_data = json.load(fc)
        except json.JSONDecodeError as e:
            self.logger.error(f'JSONDecodeError:{e}')
            exit(e)
        except FileNotFoundError as e:
            self.logger.error(f'FileNotFoundError:{e}')
            exit(e)
