"""
Intricate Chat Bot for Twitch.tv with Whispers

By Shane Engelman <me@5h4n3.com>
"""

import json
import re
import sys
import time

import globals
import lib.functions_commands as commands
import requests
import src.config.crons as crons
import src.lib.command_headers
import src.lib.rive as rive
import src.lib.twitch as twitch
from lib.functions_general import pbot
from src.config.config import channels_to_join, config
from src.lib.queries import Database
from twisted.internet import reactor, task, threads
from twisted.internet.protocol import ClientFactory
from twisted.words.protocols import irc

Database().initiate()
pattern = re.compile('[\W_]+')

reload(sys)
sys.setdefaultencoding("utf8")

PRIMARY_CHANNEL = "outerheaven"
BOT_USER = "nano_machina"
SUPERUSER = "singlerider"
TEST_USER = "theepicsnail_"

SERVER = config["server"]
NICKNAME = config["username"]
PASSWORD = config["oauth_password"]

ECHOERS = {}


class Bot(irc.IRCClient):

    def __init__(self):
        self.nickname = NICKNAME
        self.password = PASSWORD
        self.config = config
        self.crons = crons.crons.get("crons", {})
        src.lib.command_headers.initalizeCommands(config)

    def dataReceived(self, data):
        if "PING" not in str(data).split()[0] and "PONG" not in str(data).split()[1]:
            print("->*" + data)
        if data.split()[1] == "WHISPER":
            user = data.split()[0].lstrip(":")
            channel = user.split("!")[0]
            msg = " ".join(data.split()[3:]).lstrip(":")
            self.whisper(user, channel, msg)
        irc.IRCClient.dataReceived(self, data)

    def signedOn(self):
        print("\033[91mYOLO, I was signed on to the server!!!\033[0m")
        if self.factory.kind == "whisper":
            self.sendLine("CAP REQ :twitch.tv/commands")
        if self.factory.kind == "chat":
            for channel in channels_to_join:
                self.joinChannel(channel)
        ECHOERS[self.factory.kind] = self

    def joinChannel(self, channel):
        self.join(channel)
        return

    def joined(self, channel):
        if self.factory.kind == "chat":
            self.cron_initialize(BOT_USER, channel)

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        if self.kind == "whisper":
            whisper_url = "http://tmi.twitch.tv/servers?cluster=group"
            whisper_resp = requests.get(url=whisper_url)
            whisper_data = json.loads(whisper_resp.content)
            socket = whisper_data["servers"][0].split(":")
            WHISPER = [str(socket[0]), int(socket[1])]
            reactor.connectTCP(WHISPER[0], WHISPER[1], BotFactory("whisper"))
        else:
            connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()

    def action(self, user, channel, data):
        pass

    def privmsg(self, user, channel, message):
        """Called when the bot receives a message."""
        username = user.split("!")[0].lstrip(":")
        globals.CURRENT_USER = username
        chan = channel.lstrip("#")
        globals.CURRENT_CHANNEL = chan
        chan = channel.lstrip("#")
        # TODO add spam detector here
        chan = channel.lstrip("#")
        if message[0] == "!":
            message_split = message.split()
            fetch_command = Database().get_command(message_split[0], chan)
            if fetch_command and len(fetch_command) > 0:
                if message_split[0] == fetch_command[3]:
                    self.return_custom_command(
                        channel, message_split, username, fetch_command)
                    return
        part = message.split(' ')[0]
        valid = False
        if commands.is_valid_command(message):
            valid = True
        if commands.is_valid_command(part):
            valid = True
        if not valid:
            return
        resp = self.handle_command(
            part, channel, username, message)
        if resp:
            self.msg(channel, resp.replace("\n", "").replace("\r", "") + "\r\n")

    def whisper(self, user, channel, msg):
        msg = msg.lstrip("!")
        if "!" not in user:
            channel = user
            resp = msg
            username = user
        else:
            username = user.split("!")[0].lstrip(":")
            resp = rive.Conversation(self).run(BOT_USER, username, msg)[:350]
        if "ERR" in resp:
            resp = "Try again. I dropped my glasses."
        sender = "{user}!{user}@{user}.tmi.twitch.tv".format(user=BOT_USER)
        line = ":{user} PRIVMSG {channel} :{message}".format(
            user=sender, channel=channel, message=resp)
        echoer = ECHOERS["whisper"]
        echoer.sendLine(line)

    def return_custom_command(self, channel, message, username, fetch_command):
        chan = channel.lstrip("#")
        replacement_user = username
        response = str(fetch_command[4])
        if len(message) > 1:
            replacement_user = message[1]
        resp = str(response.replace(
            "{}", replacement_user).replace("[]", str(fetch_command[5] + 1)))
        if fetch_command[6] == "mod":
            moderator = Database().get_moderator(username, chan)
            if moderator:
                self.msg(channel, resp)
                Database().increment_command(message[0], chan)
        elif fetch_command[6] == "reg":
            self.msg(channel, resp)
            Database().increment_command(message[0], chan)

    def cron_initialize(self, user, channel):
        crons = self.crons.get("#" + channel.lstrip("#"), None)
        if crons:
            for job in crons:
                if job[1]:
                    kwargs = {"delay": job[0], "callback": job[2], "channel": channel}

                    def looping_call(kwargs):
                        time.sleep(kwargs["delay"])
                        task.LoopingCall(self.cron_job, kwargs).start(kwargs["delay"])
                    threads.deferToThread(looping_call, kwargs)
                    continue

    def cron_job(self, kwargs):
        channel = kwargs["channel"]
        resp = kwargs["callback"](kwargs["channel"])
        if resp:
            user = "{user}!{user}@{user}.tmi.twitch.tv".format(user=BOT_USER)
            line = ":{user} PRIVMSG {channel} :{message}".format(
                user=user, channel=channel, message=resp)
            print "<*>" + line
            self.transport.write(line + "\r\n")

    def handle_command(self, command, channel, username, message):
        db = Database()
        is_active = db.get_active_command(
            channel=channel.lstrip("#"), command=command)[0]
        if is_active == 0:
            return
        if command == message:
            args = []
        elif command == message and command in commands.keys():  # pragma: no cover
            pass
        else:
            args = [message[len(command) + 1:]]
        if not commands.check_is_space_case(command) and args:
            args = args[0].split(" ")
        if commands.is_on_cooldown(command, channel):
            pbot('Command is on cooldown. ({0}) ({1}) ({2}s remaining)'.format(
                command, username, commands.get_cooldown_remaining(
                    command, channel)), channel)
            self.whisper(
                username, channel,  "Sorry! " + command +
                " is on cooldown for " + str(
                    commands.get_cooldown_remaining(
                        command, channel)
                ) + " more seconds in " + channel.lstrip("#") +
                ". Can I help you?")
            return
        if commands.check_has_user_cooldown(command):
            if commands.is_on_user_cooldown(command, channel, username):
                self.whisper(
                    username, channel, "Slow down! Try " + command +
                    " in " + channel.lstrip("#") + " in another " + str(
                        commands.get_user_cooldown_remaining(
                            command, channel, username)) + " seconds or just \
ask me directly?")
                return
            commands.update_user_last_used(command, channel, username)
        cmd_return = commands.get_return(command)
        if cmd_return != "command":
            resp = '(%s) : %s' % (username, cmd_return)
            commands.update_last_used(command, channel)
            self.msg(channel, resp)
            return
        if commands.check_has_ul(username, command):
            user_data, __ = twitch.get_dict_for_users(channel)
            try:
                moderator = Database().get_moderator(username, channel.lstrip("#"))
                if not moderator and username != SUPERUSER:
                    resp = '(%s) : %s' % (
                        username, "This is a moderator-only command!")
                    pbot(resp, channel)
                    self.msg(channel, resp)
                    return
            except Exception as error:  # pragma: no cover
                with open("errors.txt", "a") as f:
                    error_message = "{0} | {1} : {2}\n{3}\n{4}".format(
                        username, channel, command, user_data, error)
                    f.write(error_message)
        result = commands.pass_to_function(command, args)
        commands.update_last_used(command, channel)
        if result:
            resp = '(%s) : %s' % (username, result)[:350]
            pbot(resp, channel)
            return resp


class BotFactory(ClientFactory):

    def __init__(self, kind):
        self.kind = kind

    def buildProtocol(self, addr):
        bot = Bot()
        bot.factory = self
        return bot

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        if self.kind == "whisper":
            whisper_url = "http://tmi.twitch.tv/servers?cluster=group"
            whisper_resp = requests.get(url=whisper_url)
            whisper_data = json.loads(whisper_resp.content)
            socket = whisper_data["servers"][0].split(":")
            WHISPER = [str(socket[0]), int(socket[1])]
            reactor.connectTCP(WHISPER[0], WHISPER[1], BotFactory("whisper"))
        else:
            connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()
