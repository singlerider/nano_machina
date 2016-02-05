from src.lib.queries import Database
from src.lib.twitch import get_stream_game
import globals


def addquote(args):
    db = Database()
    user = globals.CURRENT_USER
    channel = globals.CURRENT_CHANNEL
    quote = unicode(args[0].strip().strip("\"").strip("\'"), 'utf-8')
    if len(quote) > 300:
        return "Let's keep it below 300 characters?"
    game = get_stream_game(channel)
    db.add_quote(channel, user, quote, game)
    return "{0} added!".format(quote)
