import os
import sys
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
from aspen_pyconnect import IP21Connector

from list_H160 import TAGS, unit_name

TIME_DELTA = 7
QUERY_PERIOD = '00:1:00'
res = []

load_dotenv()

try:
    time_delta = int(sys.argv[1]) if len(sys.argv) > 1 else TIME_DELTA
except ValueError:
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(
            "Pass number of days for report as parameter like 'python main.py 30'\nCalling without arguments will "
            "generate report for one week by default "
        )
        quit()

    print(f"time delta param should be int, processing with default time delta={TIME_DELTA}")
    time_delta = TIME_DELTA

aspen = IP21Connector(
    server=os.environ.get("SERVER"),
    user=os.environ.get("USER"),
    pw=os.environ.get("PASS"),
)
aspen.connect()


def query(tag_name, delta):
    start_time = datetime.today() - timedelta(days=delta)
    data = aspen.history(
        start_time=start_time,
        end_time=datetime.now(),
        tag_name=tag_name,
        period=QUERY_PERIOD,
        stepped=0,
        request=2
    )
    return data


m = pd.DataFrame()

for tag in TAGS:
    res = query(tag, time_delta)

    df = pd.DataFrame(data=res, columns=['utc_time', 'value'])
    df.rename(columns={'value': tag}, inplace=True)
    df['utc_time'] = pd.to_datetime(df['utc_time'], utc=True)
    df.to_csv(f"data/row/{tag}.csv", sep=',', index=False)

    if len(m) == 0:
        m = df
    else:
        m = pd.merge_asof(m, df, on=['utc_time'], tolerance=pd.Timedelta('30s'), direction='nearest')

m.to_csv(f"./data/{unit_name}.csv", sep=',', index=False)
