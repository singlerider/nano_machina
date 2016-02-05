from src.lib.queries import Database
import src.lib.twitch as twitch


class ChannelData:

    def __init__(self, channel):
        self.channel = channel
        self.db = Database()

    def get_channel_id_from_twitch(self):
        channel_id = twitch.get_channel_id(self.channel)
        return channel_id

    def get_stream_id_from_twitch(self):
        stream_id = twitch.get_stream_id(self.channel)
        return stream_id

    def get_channel_id_from_db(self):
        channel_id = self.db.get_channel_id(self.channel)
        return channel_id

    def get_stream_id_from_db(self):
        stream_id = self.db.get_stream_id(self.channel)
        return stream_id

    def add_channel_id(self, channel_id):
        self.db.add_channel_id(channel_id, self.channel)

    def update_stream_id(self, stream_id):
        self.db.update_stream_id(self.channel, stream_id)

    def get_channel_data_by_user(self, user, data_type):
        channel_data = self.db.get_channel_data_by_user(user,
                                                        self.channel, data_type)
        return channel_data

    def get_channel_data_by_data_type(self, data_type):
        channel_data = self.db.get_channel_data_by_data_type(self.channel,
                                                          data_type)
        return channel_data

    def insert_channel_data(self, user, data_type):
        self.db.insert_channel_data(user, self.channel, data_type)

    def remove_channel_data(self, data_type):
        self.db.remove_channel_data(self.channel, data_type)
