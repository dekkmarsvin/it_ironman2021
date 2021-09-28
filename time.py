import pytz
from datetime import datetime, timezone
from tzlocal import get_localzone

utc_dt = datetime.now(timezone.utc)

PST = pytz.timezone('US/Pacific')
EST = pytz.timezone('US/Eastern')
JST = pytz.timezone('Asia/Tokyo')
NZST = pytz.timezone('Pacific/Auckland')
TWT = pytz.timezone('Asia/Taipei')

print("Pacific time {}".format(utc_dt.astimezone(PST).isoformat()))
print("Eastern time {}".format(utc_dt.astimezone(EST).isoformat()))
print("UTC time     {}".format(utc_dt.isoformat()))
print("Japan time   {}".format(utc_dt.astimezone(JST).isoformat()))

# Use astimezone() without an argument
print("Local time   {}".format(utc_dt.astimezone().isoformat()))

# Use tzlocal get_localzone
print("Local time   {}".format(utc_dt.astimezone(get_localzone()).isoformat()))

# Explicitly create a pytz timezone object
# Substitute a pytz.timezone object for your timezone
print("Local time   {}".format(utc_dt.astimezone(NZST).isoformat()))

ldt = datetime.fromtimestamp(1632791870594 / 1000.0)
print("TWT time   {}".format(ldt.astimezone(TWT).strftime("%Y/%m/%d %H:%M:%S")))