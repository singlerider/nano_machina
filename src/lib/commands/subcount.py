import json

import globals
import requests


def subcount(**kwargs):
    channel = kwargs.get("testchannel")
    try:
        token = globals.TWITCH_OAUTH[channel]
    except:
        return "This channel hasn't been authenticated. " + \
            "The streamer needs to head to shane.gg/twitch/authorize " + \
            "and notify singlerider"
    url = "https://api.twitch.tv/kraken/channels/" + channel + "/subscriptions"
    params = {"limit": 1}
    headers = {
        "Accept": "application/vnd.twitchtv.v3+json",
        "Authorization": "OAuth {token}".format(token=token)
    }
    try:
        resp = requests.get(url=url, headers=headers, params=params)
        data = json.loads(resp.content)
        sub_count = data["_total"]
        return sub_count
    except Exception as error:
        print error
        return "There was a problem."
