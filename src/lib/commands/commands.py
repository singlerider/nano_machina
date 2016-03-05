import src.lib.command_headers as headers


def commands(**kwargs):
    return str(", ".join(sorted(headers.commands))).replace("!", "")
