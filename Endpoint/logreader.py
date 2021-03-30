import win32evtlog # requires pywin32 pre-installed
import datetime
import xmltodict
import sqlite3

count = 0

today_time = datetime.datetime.now()

query = "<QueryList>\
  <Query Id=\"0\" Path=\"Microsoft-Windows-Sysmon/Operational\">\
    <Select Path=\"Microsoft-Windows-Sysmon/Operational\">\
      *[System[TimeCreated[@SystemTime&gt;='2021-03-29T20:30:33.000Z' and @SystemTime&lt;='2021-03-29T20:40:33.999Z']]]\
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
            evtID = int(record_dict['Event']['System']['EventID'])
            
            #print(record_dict['Event']['EventData']['Data'][4]['#text'])
            # for data in record_dict['Event']['EventData']['Data']:
            #   print(data['@Name']+":"+data['#text'])

            if evtID == 1:
              vals = []
              for data in record_dict['Event']['EventData']['Data']:
                # vals.append(data['@Name'])
                vals.append(data['#text'])
              con = sqlite3.connect('RedAlert.db')
              cur = con.cursor()
              # print(vals)
              
              cur.execute("""INSERT INTO evt1_processCreate VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(str(vals[0]),str(vals[1]),str(vals[2]),str(vals[3]),str(vals[4]),str(vals[5]),str(vals[6]),str(vals[7]),str(vals[8]),str(vals[9]),str(vals[10]),str(vals[11]),str(vals[12]),str(vals[13]),str(vals[14]),str(vals[15]),str(vals[16]),str(vals[17]),str(vals[18]),str(vals[19]),str(vals[20]),str(vals[21])))
              
              con.commit()
              con.close()
              
            if evtID == 2:
              pass
            if evtID == 3:
              vals = []
              for data in record_dict['Event']['EventData']['Data']:
                # vals.append(data['@Name'])
                vals.append(data['#text'])
              con = sqlite3.connect('RedAlert.db')
              cur = con.cursor()
              # print(vals)
              cur.execute("""INSERT INTO evt3_networkConnect VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(str(vals[0]),str(vals[1]),str(vals[2]),str(vals[3]),str(vals[4]),str(vals[5]),str(vals[6]),str(vals[7]),str(vals[8]),str(vals[9]),str(vals[10]),str(vals[11]),str(vals[12]),str(vals[13]),str(vals[14]),str(vals[15]),str(vals[16]),str(vals[17])))
              
              con.commit()
              con.close()
              #   # print(data['@Name']+":"+data['#text'])
            if evtID == 4:
              vals = []
              for data in record_dict['Event']['EventData']['Data']:
                # vals.append(data['@Name'])
                vals.append(data['#text'])
              con = sqlite3.connect('RedAlert.db')
              cur = con.cursor()
              # print(vals)
              cur.execute("""INSERT INTO evt4_sysmonState VALUES(?,?,?,?)""",(str(vals[0]),str(vals[1]),str(vals[2]),str(vals[3])))
             
              con.commit()
              con.close()
            if evtID == 5:
              vals = []
              for data in record_dict['Event']['EventData']['Data']:
                # vals.append(data['@Name'])
                vals.append(data['#text'])
              con = sqlite3.connect('RedAlert.db')
              cur = con.cursor()
              # print(vals)
              cur.execute("""INSERT INTO evt5_processTerminate VALUES(?,?,?,?,?)""",(str(vals[0]),str(vals[1]),str(vals[2]),str(vals[3]),str(vals[4])))
                           
              con.commit()
              con.close()
            if evtID == 6:
              pass
            if evtID == 7:
              pass
            if evtID == 8:
              pass
            if evtID == 9:
              pass
            if evtID == 10:
              pass
            if evtID == 11:
              pass
            if evtID == 12:
              pass
            if evtID == 13:
              pass
            if evtID == 14:
              pass
            if evtID == 15:
              pass
            if evtID == 16:
              vals = []
              for data in record_dict['Event']['EventData']['Data']:
                # vals.append(data['@Name'])
                vals.append(data['#text'])
              con = sqlite3.connect('RedAlert.db')
              cur = con.cursor()
              # print(vals)

              cur.execute("""INSERT INTO evt16_sysmonConfigChange VALUES(?,?,?)""",(str(vals[0]),str(vals[1]),str(vals[2])))
            
              con.commit()
              con.close()
            if evtID == 17:
              pass
            if evtID == 18:
              pass
            if evtID == 19:
              pass
            if evtID == 20:
              pass
            if evtID == 21:
              pass
            if evtID == 22:
              vals = []
              for data in record_dict['Event']['EventData']['Data']:
                # vals.append(data['@Name'])
                vals.append(data['#text'])
              con = sqlite3.connect('RedAlert.db')
              cur = con.cursor()
              # print(vals)
              
              cur.execute("""INSERT INTO evt22_dnsLookup VALUES(?,?,?,?,?,?,?,?)""",(str(vals[0]),str(vals[1]),str(vals[2]),str(vals[3]),str(vals[4]),str(vals[5]),str(vals[6]),str(vals[7])))

              con.commit()
              con.close()

            if evtID == 23:
              pass
            

            
            # for data in record_dict['Event']:
            #   # print(data['System'])
            #   # print(data['EventData'])
            #   print(data)
            #   print("----------")

            print("-----------------------"+str(record_dict['Event']['System']['EventRecordID'])+"-----------------------")