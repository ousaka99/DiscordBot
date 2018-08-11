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


def debug_bot_command_luck():
    luck_results = []
    for n in range(0, 100):
        words = []
        result = command.bot_command_luck_choice(words)
        choice = result[0]
        luck_results.append(choice)

    c = collections.Counter(luck_results)
    print(c)


debug_bot_command_luck()
