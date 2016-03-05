import src.lib.command_headers as commands
from src.lib.queries import Database


def deactivate(args, **kwargs):
    channel = kwargs.get("channel", "testchannel")
    command = "!" + args[0].lstrip("!")
    command_data = commands.commands.get(command, None)
    if command == "!activate" or command == "!deactivate":
        return "You can't do that."
    if command_data:
        db = Database()
        db.modify_active_command(channel=channel, command=command, active=0)
        return command + " deactivated!"
    else:
        return command + " not found."
