"""
Custom Twitch Chat Moderator Bot for Twitch.tv

By Shane Engelman me@5h4n3.com @shaneengelman

Made for the Outer Heaven Network at twitch.tv/uknighted
"""

import sys

import globals
import lib.functions_commands as commands
import lib.irc as irc_
import src.config.crons as crons
import src.lib.command_headers
import src.lib.cron as cron
import src.lib.twitch as twitch
from lib.functions_general import *
from src.lib.queries import Database
from src.lib.twitch import get_dict_for_users

reload(sys)
sys.setdefaultencoding("utf8")


END = False

BOT_USER = "nano_machina"
TEST_USER = "singlerider"
STREAM_USER = "uknighted"


class Bot(object):

    def __init__(self, config):
        self.db = Database()
        self.db.initiate()
        self.config = config
        self.crons = crons
        src.lib.command_headers.initalizeCommands(config)
        self.irc = irc_.irc(config)
        # start threads for channels that have cron messages to run
        cron.initialize_crons(self.irc, self.crons.crons.get("crons", {}))
        cron.initialize_channel_id_check(self.config)
        globals.irc = self.irc

    def run(self):

        def check_for_sub(channel, username, message):
            db = Database()
            try:
                channel = channel.lstrip("#")
                message_split = message.rstrip("!").split()
                subbed_user = message_split[0].lower()
                if message_split[1] == "just" and len(message_split) < 4:
                    points = 1000
                    db.add_user([subbed_user], channel)
                    db.modify_points(subbed_user, channel, points)
                    resp = "/me {0} just subscribed for the first time!\
 {1} cash for you!".format(subbed_user, points)
                    self.irc.send_message("#" + channel, resp)
                elif message_split[1] == "subscribed" and len(message_split) < 9:
                    months_subbed = message_split[3]
                    points = 250
                    db.add_user([subbed_user], channel)
                    db.modify_points(subbed_user, channel, points)
                    resp = "/me {0} has just resubscribed for {1} months \
straight and is getting {2} cash!".format(subbed_user, months_subbed, points)
                    self.irc.send_message("#" + channel, resp)
            except Exception as error:
                print error

        def custom_command(channel, message, username, elements):
            db = Database()
            command = elements[3]
            chan = channel.lstrip("#")
            replacement_user = username
            if len(message) > 1:
                replacement_user = message[1]
            if elements[6] == "mod":
                user_dict, __ = get_dict_for_users()
                if username in user_dict["chatters"]["moderators"]:
                    resp = elements[4].replace("{}", replacement_user)
                    self.irc.send_message(channel, resp)
                    db.increment_command(command, chan)
                else:
                    resp = "This is a moderator-only command"
                    self.irc.send_message(channel, resp)
            elif elements[6] == "reg":
                resp = elements[4].replace("{}", replacement_user)
                self.irc.send_message(channel, resp)
                db.increment_command(command, chan)

        while True:
            try:
                data = self.irc.nextMessage()
                if not self.irc.check_for_message(data):
                    continue
                message_dict = self.irc.get_message(data)
                channel = message_dict['channel']
                globals.CURRENT_CHANNEL = channel.lstrip('#')
                message = message_dict['message']  # .lower()
                username = message_dict['username']
                globals.CURRENT_USER = username
                chan = channel.lstrip("#")
                if message[0] == "!":
                    command = message.split(" ")[0]
                    command_data = self.db.get_command(command, chan)
                    if command_data:
                        message_split = message.split(" ")
                        custom_command(
                            channel, message_split, username, command_data)
                if username == "twitchnotify":
                    check_for_sub(channel, username, message)
                part = message.split(' ')[0]
                valid = False
                if commands.is_valid_command(message):
                    valid = True
                if commands.is_valid_command(part):
                    valid = True
                if not valid:
                    continue
                self.handleCommand(part, channel, username, message)
            except Exception as error:
                print error

    def handleCommand(self, command, channel, username, message):
        # parse arguments
        # if command is space case then
        #   !foo bar baz
        # turns into
        #   command = "!foo", args=["bar baz"]
        # otherwise it turns into
        #   command = "!foo", args=["bar", "baz"]
        # print("Inputs:", command, channel, username, message)
        if command == message:
            args = []
        else:
            # default to args = ["bar baz"]
            args = [message[len(command) + 1:]]
        if not commands.check_is_space_case(command) and args:
            # if it's not space case, break the arg apart
            args = args[0].split(" ")
        if commands.is_on_cooldown(command, channel):
            pbot('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
                command, username, commands.get_cooldown_remaining(
                    command, channel)), channel)
            return
        if commands.check_has_user_cooldown(command):
            if commands.is_on_user_cooldown(command, channel, username):
                resp = "Sorry! You've got " + str(
                    commands.get_user_cooldown_remaining(
                        command, channel, username)) + \
                    " seconds before you can do that again, " + username + "!"
                self.irc.send_message(channel, resp)
                return
            commands.update_user_last_used(command, channel, username)
        pbot('Command is valid and not on cooldown. (%s) (%s)' %
             (command, username), channel)
        # Check for and handle the simple non-command case.
        cmd_return = commands.get_return(command)
        if cmd_return != "command":
            # it's a return = "some message here" kind of function
            resp = '(%s) : %s' % (username, cmd_return)
            commands.update_last_used(command, channel)
            self.irc.send_message(channel, resp)
            return
        # if there's a required userlevel, validate it.
        if commands.check_has_ul(username, command):
            user_data, __ = twitch.get_dict_for_users(channel)
            try:
                if username not in user_data["chatters"]["moderators"]:
                    if username != TEST_USER:
                        resp = '(%s) : %s' % (
                            username, "This is a moderator-only command!")
                        pbot(resp, channel)
                        self.irc.send_message(channel, resp)
                        return
            except Exception as error:
                with open("errors.txt", "a") as f:
                    error_message = "{0} | {1} : {2}\n{3}\n{4}".format(
                        username, channel, command, user_data, error)
                    f.write(error_message)
        approved_channels = [STREAM_USER, BOT_USER, TEST_USER]
        if globals.CURRENT_CHANNEL not in approved_channels:
            prevented_list = []
            if command.lstrip("!") in prevented_list:
                return
        result = commands.pass_to_function(command, args)
        commands.update_last_used(command, channel)
        if result:
            resp = '(%s) : %s' % (username, result)
            pbot(resp, channel)
            self.irc.send_message(channel, resp)
