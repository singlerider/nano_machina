import globals
import src.lib.command_headers as commands
from src.lib.queries import Database

def activate(args):
    channel = globals.CURRENT_CHANNEL
    command = "!" + args[0].lstrip("!")
    command_data = commands.commands.get(command, None)
    if command == "!activate" or command == "!deactivate":
        return "You can't do that."
    if command_data:
        db = Database()
        db.modify_active_command(channel=channel, command=command, active=1)
        return command + " activated!"
    else:
        print command, command_data, commands
        return command + " not found."
