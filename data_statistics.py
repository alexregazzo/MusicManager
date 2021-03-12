from __future__ import annotations
import database.objects
import datetime
import utils
import typing


def hourlyStats(tokenapp: database.objects.TokenApp, timezoneOffsetMinutes: int) -> typing.List[float]:
    histories = database.objects.History.getAll(use_username=tokenapp.use_username)
    hours = [0 for _ in range(24)]
    for history in histories:
        dt = utils.parse_datetime(history.his_played_at).replace(tzinfo=datetime.timezone.utc)
        timestamp = dt.timestamp() - timezoneOffsetMinutes * 60
        i = int(timestamp / 3600 % 24)
        hours[i] += 10000
    return [int(x / len(histories)) / 10000 for x in hours]


def weekdayStats(tokenapp: database.objects.TokenApp, timezoneOffsetMinutes: int) -> typing.List[float]:
    histories = database.objects.History.getAll(use_username=tokenapp.use_username)
    weekdays = [0 for _ in range(7)]  # 0 on monday
    for history in histories:
        dt = utils.parse_datetime(history.his_played_at).replace(tzinfo=datetime.timezone.utc) - datetime.timedelta(
            minutes=timezoneOffsetMinutes)
        weekdays[dt.weekday()] += 10000
    return [int(x / len(histories)) / 10000 for x in weekdays]
