import datetime as dt

now = dt.datetime.now()
local_now = now.astimezone()
local_tz = local_now.tzinfo
local_tzname = local_tz.tzname(local_now)
print(local_tzname)
print(dt.datetime.now())