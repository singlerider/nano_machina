from src.lib.queries import Database
import globals


def rem(args):
    db = Database()
    command = args[0].lower()
    channel = globals.CURRENT_CHANNEL
    command_data = db.get_command(command, channel)
    if command_data:
        db.remove_command(command, channel)
        return "{0} removed!".format(
            command)
    else:
        return "{0} not found.".format(command)
