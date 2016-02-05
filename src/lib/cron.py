import time
from threading import Thread
from src.lib.channel_data import ChannelData


def initialize_channel_id_check(config):
    for channel in config["channels"]:
        channel = channel.lstrip("#")
        ThreadJob().check_channel_id(channel)


def initialize_crons(irc, crons):
    # start up the cron jobs.
    # config should be in the structure of
    # {
    #   "#channel": [ (period, enabled, callback),.... ]
    #   ...
    # }
    for channel, jobs in crons.items():
        # jobs can be [], False, None...
        if not jobs:
            continue
        for (delay, enabled, callback) in jobs:
            if not enabled:
                continue
            CronJob(irc, channel, delay, callback).start()


class CronJob(Thread):

    def __init__(self, irc, channel, delay, callback):
        Thread.__init__(self)
        self.daemon = True
        self.delay = delay
        self.callback = callback
        self.irc = irc
        self.channel = channel

    def run(self):
        while True:
            time.sleep(self.delay)
            self.irc.send_message(self.channel, self.callback(self.channel))

class ThreadJob(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def check_channel_id(self, channel):
        cd = ChannelData(channel)
        if not cd.get_channel_id_from_db():
            channel_id = cd.get_channel_id_from_twitch()
            cd.add_channel_id(channel_id)
