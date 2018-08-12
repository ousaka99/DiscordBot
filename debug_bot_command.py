import bot_command
import bot_config
import logging.config
import collections

# <editor-fold desc="setting">
logging.config.fileConfig("logging.conf")
logger = logging.getLogger()
config = bot_config.BotConfig()
command = bot_command.BotCommand(logger, config)
commandUsers = []
# </editor-fold>


def debug_bot_command_tier(words):
    words.insert(0, 'dummy_cmd')
    tier_results = []
    for n in range(0, 1000):
        result = command.bot_command_tier_execute(words)
        tier = result[0]
        tier_results.append(tier)

    c = collections.Counter(tier_results)
    print(c)


def debug_bot_command_ship(words):
    words.insert(0, 'dummy_cmd')
    ships_results = []
    for n in range(0, 1000):
        result = command.bot_command_ship_execute(words)
        ships = result[0]
        ships_results.extend(ships)

    c = collections.Counter(ships_results)
    print(c)


def debug_bot_command_choice(words):
    words.insert(0, 'dummy_cmd')
    choice_results = []
    for n in range(0, 1000):
        result = command.bot_command_choice_execute(words)
        choice = result[0]
        choice_results.append(choice)

    c = collections.Counter(choice_results)
    print(c)


def debug_bot_command_pickup(words):
    words.insert(0, 'dummy_cmd')
    pickups_results = []
    for n in range(0, 1000):
        result = command.bot_command_pickup_execute(words)
        pickups = result[0]
        pickups_results.extend(pickups)

    c = collections.Counter(pickups_results)
    print(c)


def debug_bot_command_luck(words):
    words.insert(0, 'dummy_cmd')
    luck_results = []
    for n in range(0, 1000):
        words = []
        result = command.bot_command_luck_execute(words)
        choice = result[0]
        luck_results.append(choice)

    c = collections.Counter(luck_results)
    print(c)


# debug_bot_command_tier(['1', '10'])


# debug_bot_command_ship(['8', '8', '1', 'DD日'])


debug_bot_command_choice(['Ａ', 'Ｂ', 'Ｃ', 'Ｄ', 'Ｅ'])


# debug_bot_command_pickup(['2', 'Ａ', 'Ｂ', 'Ｃ', 'Ｄ', 'Ｅ'])


# debug_bot_command_luck([''])
