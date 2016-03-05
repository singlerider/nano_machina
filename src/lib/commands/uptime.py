from src.lib.twitch import *


def uptime(**kwargs):
    uptime = get_stream_uptime()
    channel = kwargs.get("channel", "testchannel")
    if get_stream_status():
        return "The current !uptime is " + str(uptime)
    else:
        return channel + " is offline."
