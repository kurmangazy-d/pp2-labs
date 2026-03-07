import sys
from datetime import datetime, timezone, timedelta

def to_utc(line):
    time_str, tz = line.rsplit(" ", 1)
    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

    sign = -1 if tz[3] == '-' else 1
    h, m = map(int, tz[4:].split(":"))

    offset = timezone(timedelta(hours=sign * h, minutes=sign * m))
    return dt.replace(tzinfo=offset).astimezone(timezone.utc)

start = to_utc(sys.stdin.readline())
end = to_utc(sys.stdin.readline())

print(int((end - start).total_seconds()))