global config

username = 'YOURUSERNAME'
oauth_password = 'oauth:6yc3lsd1ho0jmw52vr58udcy2mqe32'
channels_to_join = ['#CHANNELTOJOIN']

for channel in channels_to_join:
    channel = channel.lstrip('#')

config = {
    # details required to login to twitch IRC server
    'server': 'irc.twitch.tv',
    'port': 6667,
    'username': username,
    # get this from http://twitchapps.com/tmi/
    'oauth_password': oauth_password,

    'debug': True,
    'log_messages': True,

    'channels': channels_to_join,
}
