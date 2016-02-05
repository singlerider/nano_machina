from src.lib.queries import Database
import src.lib.command_headers as command_headers
import globals


def edit(args):
    db = Database()
    command = args[0].lower()
    user_level = args[1]
    response = " ".join(args[2:])
    creator = globals.CURRENT_USER
    channel = globals.CURRENT_CHANNEL
    if command[0] is "!":
        if command not in command_headers.commands:
            command_data = db.get_command(command, channel)
            if command_data:
                if user_level == "reg" or user_level == "mod":
                    db.modify_command(command, response, channel, user_level)
                    return "{0} has been changed!".format(
                        command)
                else:
                    return "User level must be 'reg' or 'mod'"
            else:
                return "{0} not found.".format(command)
        else:
            return "{0} already built in to nano_machina.".format(command)
    else:
        return "Command must begin with '!'"
