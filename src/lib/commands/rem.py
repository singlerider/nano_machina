from src.lib.queries import Database


def rem(args, **kwargs):
    db = Database()
    command = args[0].lower()
    channel = kwargs.get("channel", "testchannel")
    command_data = db.get_command(command, channel)
    if command_data:
        db.remove_command(command, channel)
        return "{0} removed!".format(
            command)
    else:
        return "{0} not found.".format(command)
