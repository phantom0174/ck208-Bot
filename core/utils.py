from datetime import datetime, timezone, timedelta
from typing import Union


class Time:
    @staticmethod
    def get_info(mode) -> Union[str, int]:
        dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
        dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區

        if mode == 'whole':
            return str(dt2.strftime("%Y-%m-%d %H:%M:%S"))
        if mode == 'hour':
            return int(dt2.strftime("%H"))
        if mode == 'schedule':
            return str(dt2.strftime("%H %M"))
        if mode == 'week':
            return str(dt2.strftime("%A"))

    @staticmethod
    def in_time_range(current: str, target: str) -> bool:
        def trans(time_form):
            hour = time_form.split(' ')[0]
            minute = time_form.split(' ')[0]
            return hour * 60 + minute

        lower = trans(target.split(',')[0])
        upper = trans(target.split(',')[1])
        current = trans(current)
        if lower <= current <= upper:
            return True
        return False
