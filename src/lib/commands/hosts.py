from src.lib.twitch import *
from src.lib.channel_data import ChannelData


def hosts(**kwargs):
    channel = kwargs.get("channel", "testchannel")
    cd = ChannelData(channel)
    channel_id = cd.get_channel_id_from_db()[0]
    hosts = get_hosts(channel_id)
    return "You've got " + str(len(hosts)) + " people hosting you!"


def cron(channel):
    import globals
    try:
        channel = channel.lstrip("#")
        from src.lib.twitch import get_stream_status, get_hosts
        from src.lib.channel_data import ChannelData
        from src.lib.queries import Database
        cd = ChannelData(channel)
        if get_stream_status():
            channel_id = cd.get_channel_id_from_db()[0]
            hosts = get_hosts(channel_id)
            unthanked_users = []
            for host in hosts:
                host_data = cd.get_channel_data_by_user(host["host_login"], "host")
                if not host_data:
                    cd.insert_channel_data(host["host_login"], "host")
                    db = Database()
                    db.add_user([host["host_login"]], channel)
                    db.modify_points(host["host_login"], channel, 100)
                    unthanked_users.append(host["host_login"])
            if len(unthanked_users) == 1:
                user = unthanked_users[0]
                resp = "Thank you {0} for the host! Here's 100 cash!".format(user)
                globals.irc.send_message("#" + channel, resp)
            elif len(unthanked_users) > 1:
                resp = "The following users are receiving 100 cash for hosting: " + ", ".join(unthanked_users) + "!"
                globals.irc.send_message("#" + channel, resp)
            elif len(unthanked_users) > 10:
                resp = "Thanks to the {0} people hosting! Each of you get 100 cash!".format(
                    len(unthanked_users))
                globals.irc.send_message("#" + channel, resp)
        else:
            cd.remove_channel_data("host")
    except Exception as error:
        print error
