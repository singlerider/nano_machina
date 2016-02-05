import src.lib.commands.hosts as hosts

crons = {
    "crons": {
        "#nano_machina": [
            (300, True, hosts.cron),  # pokemon released every 20 minutes
        ],
    }
}
