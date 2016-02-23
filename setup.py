def main():
    raw_input("This is a guide to do the things to get your bot set up. \
Press Enter ")
    username = raw_input("What is your twitch username? \
Leave blank if you don't have one. Press Enter when you're done. ")
    if username == "":
        username = raw_input("Come on. Go to twitch.tv and make an account? \
Enter your username here when you're done. ")
    oauth_password = raw_input("Go to http://twitchapps.com/tmi/ and authorize \
the application. Copy the entire oauth: portion, then paste it here and \
Press Enter ")
    config_usernames = """
global config

username = '{username}'
oauth_password = '{oauth_password}'
channels_to_join = ['#{username}']
""".format(username=username, oauth_password=oauth_password)
    config_text = """
for channel in channels_to_join:
    channel = channel.lstrip('#')

config = {
    'server': 'irc.twitch.tv',
    'port': 6667,
    'username': username,
    # get this from http://twitchapps.com/tmi/
    'oauth_password': oauth_password,

    'debug': True,
    'log_messages': True,

    'channels': channels_to_join,
}
"""
    with open("src/config/config.py", "w") as f:
        f.write(config_usernames + config_text)
    raw_input("Once you exit this script, install the dependencies with \
'pip install -r requirements.txt' (prefereably from an activate virtual \
environment) and run './serve.py' Press Enter to quit ")


if __name__ == "__main__":
    main()
