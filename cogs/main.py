from discord.ext import commands
from core.cog_config import CogExtension
from core.db import JsonApi
from core.utils import Time


class Main(CogExtension):
    # ping
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f':stopwatch: {round(self.bot.latency * 1000)} (ms)')

    @commands.command()
    async def repost(self, ctx):
        if Time.get_info('hour') >= 16:
            return ctx.send(':x: 已經放學了！')

        static_schedule = JsonApi().get('StaticSetting')
        dynamic_schedule = JsonApi().get('DynamicSetting')

        announce_channel = ctx.guild.get_channel(844021342466474045)

        for index in range(7):
            if dynamic_schedule['switch_bool'][str(6 - index + 1)] is True:
                subject = static_schedule[Time.get_info("week")][str(6 - index + 1)]
                await announce_channel.send(
                    f'目前在上：\n'
                    f'{static_schedule["subject_data"][subject]}'
                )
                break

    @commands.command()
    async def next(self, ctx):
        if Time.get_info('hour') >= 16:
            return ctx.send(':x: 已經放學了！')

        static_schedule = JsonApi().get('StaticSetting')
        dynamic_schedule = JsonApi().get('DynamicSetting')

        announce_channel = ctx.guild.get_channel(844021342466474045)

        for index in range(7):
            if dynamic_schedule['switch_bool'][str(6 - index + 1)] is True:
                subject = static_schedule[Time.get_info("week")][str(6 - index + 2)]

                if subject is None:
                    return await ctx.send(':x: 現在是最後一節課了！')

                await announce_channel.send(
                    f'下一節要上：\n'
                    f'{static_schedule["subject_data"][subject]}'
                )
                break


def setup(bot):
    bot.add_cog(Main(bot))
