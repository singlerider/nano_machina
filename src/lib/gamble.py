from src.lib.queries import Database
import random
import globals
import time
from threading import Thread
import sys


def initialize(channel, user, delay, points):
    GambleThread(globals.irc, channel, delay, user, points).start()


class GambleThread(Thread):

    def __init__(self, irc, channel, delay, user, points):
        Thread.__init__(self, target=self.main)
        self.daemon = True
        self.delay = delay
        self.now = time.time()
        self.channel = "#" + channel.lstrip("#")
        self.chan = channel
        self.irc = irc
        self.user = user
        if self.channel not in globals.CHANNEL_INFO:
            globals.CHANNEL_INFO[self.chan]["gamble"] = {
                "time": None, "users": {}, "points": 0}
        globals.CHANNEL_INFO[self.chan]['gamble'] = {
            "time": time.time(), "users": {
                self.user: True}, "points": points}
        self.points = globals.CHANNEL_INFO[self.chan]['gamble']["points"]
        self.g = Gamble(self.chan, self.user, self.points)

    def main(self):
        chan = self.channel.lstrip("#")
        begin_resp = "Gambling has begun!"
        end_resp = "Gambling has finished!"
        time_left = "{0} seconds of gambling remain!".format(self.delay / 2)
        self.g.initiate_gamble()
        self.irc.send_message(self.channel, begin_resp)
        time.sleep(float(self.delay / 2))
        self.irc.send_message(self.channel, time_left)
        time.sleep(float(self.delay / 2))
        self.g.terminate_gamble()
        self.irc.send_message(self.channel, end_resp)
        participants = globals.CHANNEL_INFO[self.chan]['gamble']["users"]
        winner = random.choice(participants.keys())
        winner_points = self.points * (len(participants) - 1)
        try:
            del participants[winner]
        except KeyError:
            pass
        for participant in participants.keys():
            self.g.apply_yield(self.chan, participant, self.points * -1)
        self.g.apply_yield(self.chan, winner, winner_points)
        win_resp = "Congratulations, {0}, you won {1} cash!".format(
            winner, winner_points)
        self.irc.send_message(self.channel, win_resp)
        sys.exit()


class Gamble:

    def __init__(self, channel="testchannel", user="testuser", points=0):
        self.db = Database()
        self.channel = channel
        self.user = user
        self.points = points

    def initiate_gamble(self):
        if self.channel not in globals.CHANNEL_INFO:
            globals.CHANNEL_INFO[self.channel]["gamble"] = {
                "time": None, "users": {}, "points": 0}
        globals.CHANNEL_INFO[self.channel]['gamble'] = {
            "time": time.time(), "users": {
                self.user: True}, "points": self.points}

    def terminate_gamble(self):
        globals.CHANNEL_INFO[self.channel]['gamble']["time"] = None

    def check_gamble(self):
        if self.channel not in globals.CHANNEL_INFO:
            globals.CHANNEL_INFO[self.channel]["gamble"] = {
                "time": None, "users": {}}
        if globals.CHANNEL_INFO[self.channel]['gamble']["time"]:
            return globals.CHANNEL_INFO[self.channel]['gamble']["time"]
        else:
            return None

    def rob_yield(self, multiplier=1):
        points_yield = random.choice(range(1, 11))
        points = 0
        if points_yield > 9:
            points = random.choice(range(1, 301)) * multiplier
        elif points_yield <= 9 and points_yield > 5:
            points = random.choice(range(1, 21)) * multiplier
        elif points_yield <= 5 and points_yield > 1:
            points = random.choice(range(1, 11)) * multiplier
        else:
            points = self.points
        if bool(random.getrandbits(1)):
            points *= -1
        return points

    def apply_yield(self, channel, user, points):
        self.db.modify_points(user, channel, points)
