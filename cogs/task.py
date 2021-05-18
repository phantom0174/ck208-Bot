import discord
from discord.ext import tasks
from core.cog_config import CogExtension
from core.utils import Time
from core.db import JsonApi


class Task(CogExtension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.check_schedule.start()
        self.reset_schedule.start()

    @tasks.loop(minutes=2)
    async def check_schedule(self):
        await self.bot.wait_until_ready()

        if Time.get_info('hour') >= 18:
            return

        static_schedule = JsonApi().get('StaticSetting')
        dynamic_schedule = JsonApi().get('DynamicSetting')

        guild_208 = self.bot.get_guild(751431006132895754)
        announce_channel: discord.TextChannel = guild_208.get_channel(844021342466474045)

        for index, time_range in enumerate(static_schedule['switch']):
            if Time.in_time_range(Time.get_info('schedule'), time_range):
                if not dynamic_schedule['switch_bool'][str(index + 1)]:
                    subject = static_schedule[Time.get_info("week")][str(index + 1)]
                    await announce_channel.send(
                        f'下一節課是：\n'
                        f'{static_schedule["subject_data"][subject]}'
                    )
                    dynamic_schedule['switch_bool'][str(index + 1)] = True
                    JsonApi().put('DynamicSetting', dynamic_schedule)
                    break

    @tasks.loop(minutes=20)
    async def reset_schedule(self):
        await self.bot.wait_until_ready()

        if Time.get_info('hour') <= 18:
            return

        dynamic_schedule = JsonApi().get('DynamicSetting')

        if dynamic_schedule["reset"]:
            return

        if Time.in_time_range(Time.get_info('schedule'), '19 00,21 00'):
            for index in range(7):
                dynamic_schedule['switch_bool'][str(index + 1)] = False

            dynamic_schedule["reset"] = True
            JsonApi().put('DynamicSetting', dynamic_schedule)


def setup(bot):
    bot.add_cog(Task(bot))
