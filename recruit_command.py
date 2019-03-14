# -*- coding: utf-8 -*-

class RecruitCommand:
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config

    def bot_command_recruit_open(self, words, message, display_name):
        params = words[1:]
        options = ''
        if len(params) > 0:
            options = ' ' + ' '.join(params)
        else:
            options = ''

        msg = f'<@&{self.config.recruit_role_id}> {display_name} さんが分艦隊募集しています。{options}'

        self.logger.debug(f'role_id={self.config.recruit_role_id} '
                          f'author={display_name} '
                          f'option={options}')
        self.logger.debug(f'comment={msg}')

        return msg

    def bot_command_recruit_close(self, words, message, display_name):
        msg = f'{display_name} さんの分艦隊募集が締め切られました。'
 
        self.logger.debug(f'comment={msg}')

        return msg

    def bot_command_recruit_regist(self, words, message, display_name):
        params = words[1:]
        options = ''
        if len(params) > 0:
            options = params[0]
        else:
            options = ''
        msg = ''
        flag = ''

        if options == '':
            roles = message.author.roles
            role_flag = 'OFF'
            for role in roles:
                if (role.id == self.config.recruit_role_id):
                    role_flag = 'ON'

            msg = f'{display_name} さんの分艦隊募集通知設定は {role_flag} です。\n使い方： つうち ON / OFF'
            flag = ''
        elif options == 'ON' or options == 'on':
            msg = f'{display_name} さんの分艦隊募集通知設定を ON にしました。'
            flag = 'ON'
        elif options == 'OFF' or options == 'off':
            msg = f'{display_name} さんの分艦隊募集通知設定を OFF にしました。'
            flag = 'OFF'
        else:
            pass

        self.logger.debug(f'option={options} '
                          f'comment={msg} '
                          f'flag={flag}')

        return msg, flag

