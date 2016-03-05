from src.lib.queries import Database


def quote(**kwargs):
    db = Database()
    channel = kwargs.get("channel", "testchannel")
    # (1, u'testchannel', u'testuser', u'quote', 1, u'testgame')
    quote_data = db.get_quote(channel)
    if quote_data is None:
        return "No quotes found. Why not add one with '!addquote [quote]'?"
    else:
        quote = str(quote_data[3])
        quote_number = quote_data[4]
        game = quote_data[5]
        resp = "Quote #{0}: \"{1}\" [{2}]".format(quote_number, quote, game)
        return resp
