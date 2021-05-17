import sqlite3
import datetime
import hashlib
import json
import xmltodict
from datetime import datetime, timedelta
import time
import socket


con = sqlite3.connect('RedAlert.db')
cur = con.cursor()
cur.execute("""select * from openIOC""")
rows = cur.fetchall(); 
con.close()

time_now = datetime.utcnow()  # Or .now() for local time
prev_minute = time_now.minute - (time_now.minute % 1)
time_rounded = time_now.replace(minute=prev_minute, second=0, microsecond=0)
# print(time_now.isoformat())



def iocMatcher(data,conditions):
    req_success=len(conditions)
    actual_success=0
    # print(data)
    # print(conditions)
    for condition in conditions:
        # print(condition)
        c1=False
        c2=False
        if "negate" in str(condition) or "eventType" in str(condition):
            actual_success+=1
            continue
        if condition["token"]=="processEvent/process":
            if condition["operator"]=="equal" and data[9].lower()==condition["value"].lower():
                # print ("con1")
                actual_success+=1
            elif condition["operator"]=="contains" and condition["value"].lower() in data[9].lower():
                # print("con2")
                actual_success+=1
                
        if condition["token"]=="processEvent/processCmdLine":
            if condition["operator"]=="equal" and data[10].lower()==condition["value"].lower():
                # print("con3")
                actual_success+=1
            elif condition["operator"]=="contains" and condition["value"].lower() in data[10].lower():
                # print("con4")
                actual_success+=1

    # print(req_success)
    # print(actual_success)

    if req_success == actual_success:
        return True
    else:
        return False
              

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
    tnow=time_now.replace(second=0, microsecond=0) - timedelta(minutes=2)
    # time_now=
    tprev=time_prev.replace(second=0, microsecond=1) - timedelta(minutes=2)
    # time_prev=time_prev.replace(second=0, microsecond=1)
    print(tnow)
    print(tprev)

    print(time_now)
    print(time_prev)


    for item in rows:
        if item[1]=="process":
            # print("processtype")
            # print(item[3])
            for conditions in json.loads(item[4]):

                con = sqlite3.connect('RedAlert.db')
                cur = con.cursor()
                # query = "select * from evt1_processCreate WHERE UtcTime BETWEEN '"+str(tprev)+"' AND '"+str(tnow)+"'"
                # print(query)
                cur.execute("select * from evt1_processCreate WHERE UtcTime BETWEEN '"+str(tprev)+"' AND '"+str(tnow)+"'")
                ev = cur.fetchall(); 
                con.close()

                # print(ev)

                for data in ev:
                    # if "cert" in str(conditions) and "Cert" in data[9]:
                    #     print("yes")
                    res=iocMatcher(data,conditions)
                    if res==True:
                        print(res)
                        print(data)
                        print(conditions)
                        con = sqlite3.connect('RedAlert.db')
                        cur = con.cursor()
                        # query = "select * from evt1_processCreate WHERE UtcTime BETWEEN '"+str(tprev)+"' AND '"+str(tnow)+"'"
                        # print(query)
                        cur.execute("INSERT INTO alertDB VALUES(?,?,?,?,?,?)",("process",str(socket.gethostname()),hashlib.md5((str(data)+str(datetime.utcnow())).encode()).hexdigest(),str(datetime.utcnow()),str(data),str(item[0])))
                        con.commit()
                        con.close()
                        print("---------------")
    #         print("--------")
    # if item[1]=="file":
    #     print("filetype")

# print(rows[1][4])
# i=0
# con = sqlite3.connect('RedAlert.db')
# cur = con.cursor()
# cur.execute("""select * from evt1_processCreate""")
# ev = cur.fetchall(); 
# con.close()
# for event in ev:
#     if "bits" in str(event):
#         print(event)
#     i+=1