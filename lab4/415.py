import sys
from datetime import datetime, timezone, timedelta
import math

def parse(line):
    date, tz = line.split()
    dt = datetime.strptime(date, "%Y-%m-%d")
    sign = -1 if tz[3] == '-' else 1
    h, m = map(int, tz[4:].split(":"))
    offset = timezone(timedelta(hours=sign * h, minutes=sign * m))
    return dt, offset

def to_utc(dt, offset):
    return dt.replace(tzinfo=offset).astimezone(timezone.utc)

birth_dt, birth_tz = parse(sys.stdin.readline())
cur_dt, cur_tz = parse(sys.stdin.readline())

current = to_utc(cur_dt, cur_tz)
bmonth, bday = birth_dt.month, birth_dt.day

def next_birthday(after):
    year = after.year
    for _ in range(2):  # current year or next
        try:
            dt = datetime(year, bmonth, bday, tzinfo=birth_tz)
        except ValueError:
            dt = datetime(year, 2, 28, tzinfo=birth_tz)  # Feb 29 -> Feb 28 on non-leap
        utc = dt.astimezone(timezone.utc)
        if utc >= after:
            return utc
        year += 1
    return None

birthday = next_birthday(current)
diff_seconds = (birthday - current).total_seconds()
days = math.ceil(diff_seconds / 86400) if diff_seconds > 0 else 0
print(int(days))