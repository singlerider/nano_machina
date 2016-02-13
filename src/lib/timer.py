def cron(channel):
    try:
        from datetime import datetime, timedelta
        from src.bot import ECHOERS, BOT_USER
        from src.lib.queries import Database
        chan = channel.lstrip("#")
        now = datetime.today()
        db = Database()
        timers = db.get_timer_command(channel=chan)
        if timers:
            # channel, command, response, user_level, timer, timer_tripped, created_at
            for timer in timers:
                command = timer[1]
                resp = str(timer[2])
                minutes = timer[4]
                timer_tripped = timer[5]
                created_at = datetime.strptime(str(timer[6]), '%Y-%m-%d %H:%M:%S')
                difference = (created_at - now).seconds / 60
                if timer_tripped == 0 and difference % minutes == 0:
                    db.update_timer_command(channel=chan, command=command)
                    sender = "{user}!{user}@{user}.tmi.twitch.tv".format(
                        user=BOT_USER)
                    line = ":%s PRIVMSG %s :%s" % (sender, channel, resp)
                    echoer = ECHOERS["chat"]  # chat reactor instance
                    echoer.sendLine(line)
    except:
        pass
