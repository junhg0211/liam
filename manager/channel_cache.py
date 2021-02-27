from datetime import datetime
from json import load, dump
from typing import Optional, Dict

from discord import TextChannel, Guild
from discord.utils import get

from const import const


class ChannelCache:
    def __init__(self, server_id: int, text_channel: TextChannel, last_refer: datetime):
        self.server_id = server_id
        self.text_channel = text_channel
        self.last_refer = last_refer


class DataManager:
    def __init__(self, json_path: str = const['channel-mapping']):
        self.json_path = json_path
        self.caches: Dict[int, ChannelCache] = dict()

    async def get_channel(self, guild: Guild) -> Optional[TextChannel]:
        now = datetime.now()

        if guild.id in self.caches:
            self.caches[guild.id].last_refer = now
            return self.caches[guild.id].text_channel

        with open(self.json_path, 'r') as file:
            data = load(file)

        if str(guild.id) not in data:
            return

        text_channel = get(guild.text_channels, id=data[str(guild.id)])
        if text_channel is None:
            return

        channel_cache = ChannelCache(guild.id, text_channel, now)
        self.caches[guild.id] = channel_cache
        return text_channel

    def set_channel(self, server_id: int, text_channel_id: int):
        with open(self.json_path, 'r') as read_file:
            data = load(read_file)

        data[server_id] = text_channel_id

        with open(self.json_path, 'w') as write_file:
            dump(data, write_file)
