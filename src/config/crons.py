import src.lib.commands.hosts as hosts
import src.lib.timer as timer

crons = {
    "crons": {
        "#nano_machina": [
            (300, True, hosts.cron),
            (35, True, timer.cron),
        ],
    }
}
