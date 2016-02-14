from src.lib.queries import Database
import src.lib.command_headers as command_headers
import globals


def add(args):
    db = Database()
    command = "!" + args[0].lower().lstrip("!")
    user_level = args[1]
    response = " ".join(args[2:])
    creator = globals.CURRENT_USER
    channel = globals.CURRENT_CHANNEL
    if command not in command_headers.commands:
        if user_level == "reg" or user_level == "mod":
            db.add_command(
                user=creator, command=command, response=response,
                user_level=user_level, channel=channel)
            return "{0} added to nano_machina's custom commands!".format(
                command)
        else:
            try:
                timer = int(user_level)
                db.add_command(
                    user=creator, command=command, response=response,
                    user_level="timer", channel=channel, timer=timer)
                return "{0} added to nano_machina's custom commands!".format(
                    command)
            except Exception as error:
                print error
                return "User level must be \'reg\', \'mod\', or a number"
    else:
        return "{0} already built in to nano_machina.".format(command)
