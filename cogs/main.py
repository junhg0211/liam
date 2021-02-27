from discord import Member, VoiceState, TextChannel
from discord.ext import commands
from discord.ext.commands import Bot, Context

import log
from const import strings
from manager.channel_cache import DataManager


class Main(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.data_manager = DataManager()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if after.channel == before.channel:
            return

        if before.channel is None:
            if (text_channel := await self.data_manager.get_channel(after.channel.guild)) is None:
                return
            content = strings['joined'].format(member=member.display_name, channel=after.channel.name)

        elif after.channel is None:
            if (text_channel := await self.data_manager.get_channel(before.channel.guild)) is None:
                return
            content = strings['left'].format(member=member.display_name, channel=before.channel.name)

        else:
            if (text_channel := await self.data_manager.get_channel(after.channel.guild)) is None:
                return
            content = strings['moved'].format(
                member=member.display_name, before_channel=before.channel.name, after_channel=after.channel.name)

        await text_channel.send(content)
        log.message(content)

    @commands.command()
    async def channel(self, ctx: Context, text_channel: TextChannel):
        if text_channel is None:
            await ctx.send(strings['no-text-channel'])
            return

        self.data_manager.set_channel(ctx.guild.id, text_channel.id)
        await ctx.send(strings['text-channel-set-complete'].format(text_channel=text_channel.mention))


def setup(bot: Bot):
    bot.add_cog(Main(bot))
