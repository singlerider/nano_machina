import datetime
import json

import requests


# making this comment from Github's Oval Office


def get_dict_for_users(channel="testchannel"):
    users = {}
    channel = channel.lstrip('#')
    try:
        get_dict_for_users_url = 'http://tmi.twitch.tv/group/user/' + \
            channel + '/chatters'
        get_dict_for_users_resp = requests.get(url=get_dict_for_users_url)
        users = json.loads(get_dict_for_users_resp.content)
        user_dict = users
        all_users = []
        for user in users['chatters']['moderators']:
            all_users.append(str(user))
        for user in users['chatters']['viewers']:
            all_users.append(str(user))
        for user in users['chatters']['staff']:
            all_users.append(str(user))
        for user in users['chatters']['admins']:
            all_users.append(str(user))
        return user_dict, list(set(all_users))
    except:
        return {}, []


def user_cron(channel):
    import requests
    import json
    import globals
    channel = channel.lstrip("#")
    get_dict_for_users_url = 'http://tmi.twitch.tv/group/user/{0}/chatters'.format(
        channel)
    get_dict_for_users_resp = requests.get(url=get_dict_for_users_url)
    try:
        users = json.loads(get_dict_for_users_resp.content)
        globals.CHANNEL_INFO[channel]['viewers'] = users
    except Exception as error:
        pass


def get_stream_status(channel="testchannel"):
    get_stream_status_url = 'https://api.twitch.tv/kraken/streams/' + channel
    get_stream_status_resp = requests.get(url=get_stream_status_url)
    online_data = json.loads(get_stream_status_resp.content)
    if "stream" in online_data:
        return True
    else:
        return False


def get_stream_id(channel):
    url = 'https://api.twitch.tv/kraken/streams/' + channel
    resp = requests.get(url=url)
    data = json.loads(resp.content)
    if data["stream"] is not None:
        stream_id = data["stream"]["_id"]
        stream_id
    else:
        return None


def get_channel_game(channel):
    url = "https://api.twitch.tv/kraken/channels/" + channel
    resp = requests.get(url=url)
    data = json.loads(resp.content)
    game = data["game"]
    return game


def get_stream_game(channel):
    url = 'https://api.twitch.tv/kraken/streams/' + channel
    resp = requests.get(url=url)
    data = json.loads(resp.content)
    if data["stream"] is not None:
        return data["stream"]["game"]
    else:
        return "Offline"


def get_channel_id(channel):
    url = "https://api.twitch.tv/kraken/channels/" + channel
    try:
        resp = requests.get(url=url)
        data = json.loads(resp.content)
        channel_id = data["_id"]
    except:
        channel_id = 0
    return channel_id


def get_stream_uptime(channel="testchannel"):
    if get_stream_status(channel):
        format = "%Y-%m-%d %H:%M:%S"
        get_stream_uptime_url = 'https://api.twitch.tv/kraken/streams/' + \
            channel
        get_stream_uptime_resp = requests.get(url=get_stream_uptime_url)
        uptime_data = json.loads(get_stream_uptime_resp.content)
        start_time = str(uptime_data['stream']['created_at']).replace(
            "T", " ").replace("Z", "")
        stripped_start_time = datetime.datetime.strptime(start_time, format)
        time_delta = (datetime.datetime.utcnow() - stripped_start_time)
        return str(time_delta).split(".")[0]
    else:
        return "The streamer is offline, duh."


def get_offline_status(channel="testchannel"):
    get_offline_status_url = 'https://api.twitch.tv/kraken/streams/' + \
        channel
    get_offline_status_resp = requests.get(url=get_offline_status_url)
    offline_data = json.loads(get_offline_status_resp.content)
    if offline_data["stream"] is not None:
        return True


def get_stream_followers(channel="testchannel"):
    url = 'https://api.twitch.tv/kraken/channels/' + \
        channel + '/follows?limit=100'
    resp = requests.get(url=url)
    data = json.loads(resp.content)
    return data


def get_hosts(channel_id):
    url = "https://tmi.twitch.tv/hosts?include_logins=1&target=" + str(channel_id)
    resp = requests.get(url)
    data = json.loads(resp.content)
    hosts = data["hosts"]
    return hosts


def get_game_popularity(game):
    try:
        game_http_request = game.replace(' ', '%20')
        url = 'https://api.twitch.tv/kraken/search/streams?q=' + \
            game_http_request + '&limit=100'
        resp = requests.get(url=url)
        data = json.loads(resp.content)
        print data
        first_streamer = str(data["streams"][0]["channel"]["display_name"])
        second_streamer = str(data["streams"][1]["channel"]["display_name"])
        third_streamer = str(data["streams"][2]["channel"]["display_name"])
        first_viewers = str(data["streams"][0]["viewers"])
        second_viewers = str(data["streams"][1]["viewers"])
        third_viewers = str(data["streams"][2]["viewers"])
        top_three = first_streamer + ": " + first_viewers + ", " + second_streamer + \
            ": " + second_viewers + ", " + third_streamer + ": " + third_viewers
        return "The top three streamers playing " + game + " are: " + top_three
    except Exception as error:
        print error
        return "Avoid using special characters and check your spelling."


def get_follower_status(username="testuser", channel="testchannel"):
    try:
        url = "https://api.twitch.tv/kraken/users/{}/follows/channels/{}".format(username.lower().lstrip("@"), channel)
        resp = requests.get(url=url)
        data = json.loads(resp.content)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                  "Sep", "Oct", "Nov", "Dec"]
        suffixes = ["st", "nd", "rd", "th",]
        date_split = data["created_at"][:10].split("-")
        year = date_split[0]
        month = months[int(date_split[1]) - 1]
        day = date_split[2]
        if day[0] == "1":
            day = day + suffixes[3]
        elif day[1] == "1":
            day = day + suffixes[0]
        elif day[1] == "2":
            day = day + suffixes[1]
        elif day[1] == "3":
            day = day + suffixes[2]
        else:
            day = day + suffixes[3]
        follower_since = "{} {}, {}".format(month, day, year)
        return "{} has been following {} since {}.".format(username, channel, follower_since)
    except:
        return "{} doesn't follow {}.".format(username, channel)
