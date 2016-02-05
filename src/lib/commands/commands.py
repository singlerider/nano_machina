import src.lib.command_headers as headers


def commands():
    return str(", ".join(sorted(headers.commands))).replace("!", "")
