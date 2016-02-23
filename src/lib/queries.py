#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
test_users = ["user", "singlerider", "testuser"]


class Database:

    def __init__(self, name="twitch.db"):
        self.name = name
        self.con = lite.connect(self.name, check_same_thread=False)

    def initiate(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    username TEXT, points INT, channel TEXT);
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS custom_commands(
                    id INTEGER PRIMARY KEY, channel TEXT,
                    created_by TEXT, command TEXT,
                    response TEXT, times_used INT
                    , user_level TEXT, timer INTEGER,
                    timer_tripped INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS quotes(
                    id INTEGER PRIMARY KEY, channel TEXT,
                    created_by TEXT, quote TEXT,
                    quote_number INT, game TEXT);
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS channel_info(
                    id INTEGER PRIMARY KEY, channel TEXT,
                    stream_id INTEGER DEFAULT 0,
                    twitch_oauth TEXT DEFAULT '',
                    twitchalerts_oauth TEXT DEFAULT '');
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS channel_data(
                    id INTEGER PRIMARY KEY, channel TEXT,
                    username TEXT, data_type TEXT);
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS moderators(
                    id INTEGER PRIMARY KEY, username TEXT,
                    channel TEXT);
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS active_commands(
                    id INTEGER PRIMARY KEY, channel TEXT, command TEXT,
                    active INTEGER DEFAULT 1);
            """)

    def add_user(self, user, channel):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO users(id, username, points, channel)
                    SELECT NULL, ?, 0, ?
                    WHERE NOT EXISTS(
                        SELECT 1 FROM users WHERE username = ?
                        AND channel = ?);
            """, user, channel)

    def add_users(self, users, channel):
        user_tuples = [(user, channel, user, channel) for user in users]
        with self.con:
            cur = self.con.cursor()
            cur.executemany("""
                INSERT INTO users(id, username, points, channel)
                    SELECT NULL, ?, 0, ?
                    WHERE NOT EXISTS(
                        SELECT 1 FROM users WHERE username = ?
                        AND channel = ?);
            """, user_tuples)

    def remove_user(self, user="testuser", channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM users WHERE username = ? and channel = ?;
            """, [user, channel])

    def get_user(self, user="testuser", channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT * FROM users WHERE username = ? and channel = ?;
            """, [user, channel])
            user_data = cur.fetchone()
            return user_data

    def get_moderator(self, username, channel):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT username, channel FROM moderators
                    WHERE username = ? AND channel = ?;
            """, [username, channel])
            moderator = cur.fetchone()
            cur.close()
            return moderator

    def modify_points(self, user="testuser", channel="testchannel", points=5):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE users SET points = points + ? WHERE username = ?
                    AND channel = ?;
            """, [points, user, channel])

    def add_command(
            self, user="testuser", command="!test",
            response="{} check this out", user_level="reg",
            channel="testchannel", timer_tripped=0, timer=0):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO custom_commands(
                    id, channel, created_by, command, response,
                    times_used, user_level, timer, timer_tripped)
                    SELECT NULL, ?, ?, ?, ?, 0, ?, ?, 0
                    WHERE NOT EXISTS(
                        SELECT 1 FROM custom_commands
                            WHERE command = ? and channel = ?);
            """, [channel, user, command, response,
                        user_level, timer, command, channel])

    def remove_command(self, command="!test", channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM custom_commands
                    WHERE command = ? AND channel = ?;
            """, [command, channel])

    def modify_command(
            self, command="!test", response="different response",
            channel="testchannel", user_level="mod", timer=None):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE custom_commands SET response = ?, user_level = ?,
                    timer = ? WHERE command = ? AND channel = ?;
            """, [response, user_level, timer, command, channel])

    def increment_command(self, command="!test", channel="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE custom_commands SET times_used = times_used + 1
                    WHERE command = ? AND channel = ?;
            """, [command, channel])

    def get_command(self, command="!test", channel="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT * FROM custom_commands
                    WHERE command = ? AND channel = ?;
            """, [command, channel])
            command_data = cur.fetchone()
            return command_data

    def get_timer_command(self, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT channel, command, response, user_level,
                    timer, timer_tripped, created_at FROM custom_commands
                    WHERE channel = ? AND timer_tripped = 0
                        AND user_level = 'timer';
            """, [channel])
            timers = cur.fetchall()
            cur.execute("""
                UPDATE custom_commands SET timer_tripped = 0
                    WHERE timer_tripped = 1 AND user_level = 'timer';
            """)
            return timers

    def update_timer_command(self, channel="testchannel", command="!test"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE custom_commands SET timer_tripped = 1
                    WHERE channel = ? AND command = ?
                        AND user_level = 'timer';
            """, [channel, command])

    def add_quote(
            self, channel="testchannel", user="testuser", quote="quote",
            game="testgame"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT count(0) FROM quotes WHERE channel = ?
            """, [channel])
            count = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO quotes VALUES (NULL, ?, ?, ?, ?, ?)
            """, [channel, user, quote, count + 1, game])

    def remove_quotes(self, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM quotes WHERE channel = ?
            """, [channel])

    def get_quote(self, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT * FROM quotes WHERE channel = ?
                    ORDER BY RANDOM() LIMIT 1;
            """, [channel])
            quote = cur.fetchone()
            return quote

    def get_channel_id(self, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT id, channel FROM channel_info WHERE channel = ?;
            """, [channel])
            channel_id = cur.fetchone()
            return channel_id

    def get_stream_id(self, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT channel, stream_id FROM channel_info WHERE channel = ?;
            """, [channel])
            stream_id = cur.fetchone()
            return stream_id

    def update_stream_id(self, channel="testchannel", stream_id=1234567):
        cur = self.con.cursor()
        cur.execute("""
            UPDATE channel_info SET stream_id = ? WHERE channel = ?;
        """, [stream_id, channel])

    def add_channel_id(self, id=12345, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO channel_info(
                    id, channel)
                    SELECT ?, ?
                    WHERE NOT EXISTS(
                        SELECT 1 FROM channel_info
                            WHERE channel = ?);
            """, [id, channel, channel])

    def remove_channel_info(self, id=12345, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM channel_info WHERE id = ? OR channel = ?;
            """, [id, channel])

    def get_channel_data_by_user(
            self, user="testuser", channel="testchannel", data_type="host"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT channel, username, data_type FROM channel_data
                    WHERE username = ? AND channel = ? AND data_type = ?;
            """, [user, channel, data_type])
            channel_data = cur.fetchall()
            return channel_data

    def get_channel_data_by_data_type(
            self, channel="testchannel", data_type="host"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT id, channel, username, data_type FROM channel_data
                    WHERE channel = ? AND data_type = ?
            """, [channel, data_type])
            channel_data = cur.fetchall()
            return channel_data

    def insert_channel_data(
            self, user="testuser", channel="testchannel", data_type="host"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO channel_data(
                    id, channel, username, data_type)
                    SELECT NULL, ?, ?, ?
                    WHERE NOT EXISTS(
                        SELECT 1 FROM channel_data
                            WHERE channel = ? AND username = ?
                            AND data_type = ?);
            """, [channel, user, data_type, channel, user, data_type])

    def remove_channel_data(self, channel="testchannel", data_type="host"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM channel_data WHERE channel = ? AND data_type = ?;
            """, [channel, data_type])

    def modify_active_command(
            self, channel="testchannel", command="testcommand", active=1):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO active_commands(
                    id, channel, command, active)
                    SELECT NULL, ?, ?, ?
                    WHERE NOT EXISTS(
                        SELECT 1 FROM active_commands
                            WHERE channel = ? AND command = ?);
            """, [channel, command, active, channel, command])
            cur.execute("""
                UPDATE active_commands SET active = ?
                    WHERE channel = ? AND command = ?;
            """, [active, channel, command])

    def get_active_command(self, channel="testchannel", command="testcommand"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT active FROM active_commands
                    WHERE channel = ? AND command = ?;
            """, [channel, command])
            active = cur.fetchone()
            if active is None:
                active = (1, )
            return active
