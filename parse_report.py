import json
import datetime

org_data = "/storage/emulated/0/Android/data/com.invisatime/cache/Debug Info.json"
with open(org_data) as f:
   raw_data = f.read()

data_dict = json.loads(raw_data)

periods = data_dict['state']['timer']['periods']

for period in periods:
    start = datetime.datetime.fromtimestamp(period['start'])
    end = datetime.datetime.fromtimestamp(period['end'])
    print(start)
    print(end)



