  
import win32evtlog # requires pywin32 pre-installed
import datetime
import xmltodict
count = 0

print("Get last 30 days history...")

today_time = datetime.datetime.now()
query = "<QueryList>\
  <Query Id=\"0\" Path=\"Microsoft-Windows-Sysmon/Operational\">\
    <Select Path=\"Microsoft-Windows-Sysmon/Operational\">\
     *[System[TimeCreated[@SystemTime&gt;='2021-03-29T20:30:25.000Z' and @SystemTime&lt;='2021-03-29T20:50:25.999Z']]]\
    </Select>\
  </Query>\
</QueryList>\
"
path = "Microsoft-Windows-Sysmon/Operational"
handle = win32evtlog.EvtQuery( # Get event log
            path,
            win32evtlog.EvtQueryReverseDirection,
            query,
            None
        )

while 1:
    events = win32evtlog.EvtNext(handle, 10)
    if len(events) == 0:
        # remove parsed events
        # win32evtlog.ClearEventLog(handle, None): Access Violation (0xC0000005)
        break
    for event in events:
        count += 1

        if count % 1 == 0:
            # print(count)
        
            record = win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml)
            ##print(event)
            # print(record)

            # xml to dict
            record_dict = xmltodict.parse(record)
            # print(record_dict['Event'])
            vals = []
            for data in record_dict['Event']['EventData']['Data']:
                vals.append(data['@Name'])
                # vals.append(data['#text'])
            print(record_dict['Event']['System']['EventID'] +","+ str(vals))
            #   con = sqlite3.connect('RedAlert.db')
            #   cur = con.cursor()
            #   # print(vals)
            #   cur.execute("INSERT INTO evt3_networkConnect VALUES ("\
            #           +'\''+str(vals[0])+'\','\
            #           +'\''+str(vals[1])+'\','\
            #           +'\''+str(vals[2])+'\','\
            #           +'\''+str(vals[3])+'\','\
            #           +'\''+str(vals[4])+'\','\
            #           +'\''+str(vals[5])+'\','\
            #           +'\''+str(vals[6])+'\','\
            #           +'\''+str(vals[7])+'\','\
            #           +'\''+str(vals[8])+'\','\
            #           +'\''+str(vals[9])+'\','\
            #           +'\''+str(vals[10])+'\','\
            #           +'\''+str(vals[11])+'\','\
            #           +'\''+str(vals[12])+'\','\
            #           +'\''+str(vals[13])+'\','\
            #           +'\''+str(vals[14])+'\','\
            #           +'\''+str(vals[15])+'\','\
            #           +'\''+str(vals[16])+'\','\
            #           +'\''+str(vals[17])+"\')")
              
            #   con.commit()
            #   con.close()






            ("INSERT INTO evt1_processCreate VALUES ("\
                      +'\''+str(vals[0])+'\','\
                      +'\''+str(vals[1])+'\','\
                      +'\''+str(vals[2])+'\','\
                      +'\''+str(vals[3])+'\','\
                      +'\''+str(vals[4])+'\','\
                      +'\''+str(vals[5])+'\','\
                      +'\''+str(vals[6])+'\','\
                      +'\''+str(vals[7])+'\','\
                      +'\''+str(vals[8])+'\','\
                      +'\''+str(vals[9])+'\','\
                      +'\''+str(vals[10])+'\','\
                      +'\''+str(vals[11])+'\','\
                      +'\''+str(vals[12])+'\','\
                      +'\''+str(vals[13])+'\','\
                      +'\''+str(vals[14])+'\','\
                      +'\''+str(vals[15])+'\','\
                      +'\''+str(vals[16])+'\','\
                      +'\''+str(vals[17])+'\','\
                      +'\''+str(vals[18])+'\','\
                      +'\''+str(vals[19])+'\','\
                      +'\''+str(vals[20])+'\','\
                      +'\''+str(vals[21])+"\')")