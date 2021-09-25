import json
import datetime
from PIL import Image, ImageDraw
import sys
import math

# must be YYYYMM
# YYYYMM = sys.argv[1]

org_data = "/storage/emulated/0/Android/data/com.invisatime/cache/Debug Info.json"

# sheet info (adjustment is required if needed)
# up left
PUL = (202, 177)
# up right
PUR = (3145, 162)
# down left
PDL = (211, 2094)
# down right
PDR = (3163, 2080)
# cell width
CW = 95
# height of content
HEIGHT = 1918

# second a day
DAYSEC = 86400

with open(org_data) as f:
   raw_data = f.read()

data_dict = json.loads(raw_data)

periods = data_dict['state']['timer']['periods']

im = Image.open('./basesheet.jpg')
draw = ImageDraw.Draw(im)

def get_start_point_this_day(ut):
    # unixtime to datetime, datetime to string
    date_str = datetime.datetime.fromtimestamp(ut).strftime('%Y-%m-%d')
    YYYY = date_str.split('-')[0]
    MM = date_str.split('-')[1]
    sheet_start_point_str = '{YYYY}-{MM}-01 05:30:00'.format(YYYY=YYYY, MM=MM)
    # string to datetime
    sheet_start_point_time = datetime.datetime.strptime(sheet_start_point_str, '%Y-%m-%d %H:%M:%S')
    # datetime to unixtime
    sheet_start_point_ut = sheet_start_point_time.timestamp()
    day_count = math.floor((ut - sheet_start_point_ut)/ DAYSEC)

    start_point_this_day = sheet_start_point_ut + DAYSEC * (day_count)

    return start_point_this_day

def get_point(ut):
    '''
    get axis from unixtime
    '''
    # unixtime to datetime, datetime to string
    date_str = datetime.datetime.fromtimestamp(ut).strftime('%Y-%m-%d')
    YYYY = date_str.split('-')[0]
    MM = date_str.split('-')[1]
    sheet_start_point_str = '{YYYY}-{MM}-01 05:30:00'.format(YYYY=YYYY, MM=MM)
    # string to datetime
    sheet_start_point_time = datetime.datetime.strptime(sheet_start_point_str, '%Y-%m-%d %H:%M:%S')
    # datetime to unixtime
    sheet_start_point_ut = sheet_start_point_time.timestamp()
    day_count = math.floor((ut - sheet_start_point_ut)/ DAYSEC)
    line_x = PUL[0] + day_count * CW + CW / 2

    start_point_this_day = get_start_point_this_day(ut)
    ut_from_start = ut - start_point_this_day

    y_relative = HEIGHT * ut_from_start / DAYSEC 
    line_y = PUL[1] + y_relative

    return (line_x, line_y)

last_period_point_ut = periods[0]['start']
for period in periods:

    # remove aligner start point 
    start_point = get_point(period['start'])
    # remove aligner end point
    end_point_ut = period['end']

    draw.line((get_point(last_period_point_ut), start_point), fill=(0, 0, 255),  width=10)

    print(start_point[0], get_point(last_period_point_ut)[0])
    if start_point[0] == get_point(last_period_point_ut)[0]:
        last_period_point_ut = end_point_ut
    else:
        last_period_point_ut = get_start_point_this_day(period['start'])
       # draw.line((get_point(end_point_ut), get_point(last_period_point_ut + DAYSEC - 1)), fill=(255, 0, 0),  width=20)


im.save('out.jpg', quality=95)
