from datetime import datetime, timedelta
import time

import requests
import sqlite3
# Bootstrap by getting the most recent time that had minutes as a multiple of 1s
time_now = datetime.utcnow()  # Or .now() for local time
prev_minute = time_now.minute - (time_now.minute % 1)
time_rounded = time_now.replace(minute=prev_minute, second=0, microsecond=0)
print(time_now)
while True:
    # Wait until next 1 minute time
    time_rounded += timedelta(minutes=1)
    # print("++"+str(time_rounded))
    time_prev=time_now
    time_to_wait = (time_rounded - time_now).total_seconds()
    # print("++"+str(time_to_wait))
    time.sleep(time_to_wait)

    time_now = datetime.utcnow()  # Or .now() for local time

    # Now do whatever you want
    print(time_now.replace(second=0, microsecond=0).isoformat())
    print(time_prev.replace(second=0, microsecond=1).isoformat())

    con = sqlite3.connect('RedAlert.db')
    cur = con.cursor()
    cur.execute("select * from tConfig where key=='lastAFT'")
    trows = cur.fetchall(); 
    con.close()
    # print(trows[0][1])

    con = sqlite3.connect('RedAlert.db')
    cur = con.cursor()
    cur.execute("select * from alertDB where alert_time >'"+trows[0][1]+"'")
    rows = cur.fetchall(); 
    con.close()

    for row in rows:
        print(row)
        if row[2]!="":
            newEFT=row[3]

    print("newEFT")
    print(newEFT)

    con = sqlite3.connect('RedAlert.db')
    cur = con.cursor()
    cur.execute("update tconfig set value='"+newEFT+"' where key='lastAFT'")
    con.commit()
    con.close()

    res = requests.post('http://localhost:5000/sendAlerts', json={"data":rows})
    if res.ok:
        print(res.json())