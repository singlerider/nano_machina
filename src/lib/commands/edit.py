from src.lib.queries import Database
import src.lib.command_headers as command_headers
import globals


def edit(args):
    db = Database()
    command = "!" + args[0].lower().lstrip("!")
    user_level = args[1]
    response = " ".join(args[2:])
    creator = globals.CURRENT_USER
    channel = globals.CURRENT_CHANNEL
    if command not in command_headers.commands:
        command_data = db.get_command(command, channel)
        if command_data:
            if user_level == "reg" or user_level == "mod":
                db.modify_command(
                    command=command, response=response,
                    user_level=user_level, channel=channel, timer=None)
                return "{0} added to nano_machina's custom commands!".format(
                    command)
            else:
                try:
                    timer = int(user_level)
                    db.modify_command(
                        command=command, response=response,
                        user_level=user_level, channel=channel, timer=timer)
                    return "{0} edited to {1}!".format(
                        command, response)
                except Exception as error:
                    print error
                    return "User level must be \'reg\', \'mod\', or a number"
        else:
            return "{0} not found!".format(command)
    else:
        return "{0} already built in to nano_machina.".format(command)
