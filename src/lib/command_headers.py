import globals

commands = {
    '!commands': {
        'limit': 0,
        'return': 'command',
        'argc': 0,
        'usage': '!commands'
    },
    '!follower': {
        'limit': 0,
        'return': 'command',
        'argc': 1,
        'usage': '!follower [username]',
        'ul': 'mod'
    },
    '!uptime': {
        'limit': 15,
        'return': 'command',
        'argc': 0,
        'usage': '!uptime',
        'user_limit': 5
    },
    '!stream': {
        'limit': 60,
        'return': 'command',
        'argc': 0,
        'usage': '!stream'
    },
    '!popularity': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'space_case': True,
        'usage': '!popularity [name_of_game]'
    },
    '!follow': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'usage': '!follow [streamer_username]',
        'ul': 'mod'
    },
    '!donation': {
        'limit': 0,
        'argc': 2,
        'return': 'command',
        'usage': '!donation [username] [dollar_amount]',
        'ul': 'mod'
    },
    '!add': {
        'limit': 0,
        'argc': 3,
        'return': 'command',
        'usage': '!add [command] [user_level("mod"/"reg")/number [response]'
    },
    '!edit': {
        'limit': 0,
        'argc': 3,
        'return': 'command',
        'usage': '!edit [command] [user_level("mod"/"reg")/number] [response]'
    },
    '!rem': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'usage': '!rem [command]'
    },
    '!hosts': {
        'limit': 0,
        'return': 'command',
        'usage': '!hosts',
        'argc': 0
    },
    '!subcount': {
        'limit': 5,
        'return': 'command',
        'usage': '!subcount',
        'argc': 0,
        'user_limit': 25
    },
    '!activate': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'ul': 'mod',
        'usage': '!activate [command]'
    },
    '!deactivate': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'ul': 'mod',
        'usage': '!deactivate [command]'
    }
}

user_cooldowns = {"channels": {}}


def initalizeCommands(config):
    for channel in config['channels']:
        globals.CHANNEL_INFO[channel.lstrip("#")] = {
            "gamble": {"time": None, "users": {}}}
        user_cooldowns["channels"][channel] = {"commands": {}}
        for command in commands:
            commands[command][channel] = {}
            commands[command][channel]['last_used'] = 0
            if "user_limit" in commands[command]:
                user_cooldowns["channels"][channel]["commands"][command] = {
                    "users": {}}
