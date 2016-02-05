from src.lib.twitch import get_channel_game


def follow(args):
    name = args[0].lower().lstrip("@")
    try:
        game = get_channel_game(name)
        return "THANK YOU {0} for the support!!! Go give their page some \
love at twitch.tv/{0}, especially if you like {1}!".format(name, game)
    except:
        return "THANK YOU {0} for the support!!! Go give their page some \
love at twitch.tv/{0}!".format(name)
