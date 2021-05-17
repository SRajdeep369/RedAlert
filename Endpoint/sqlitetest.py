import sqlite3
con = sqlite3.connect('RedAlert.db')
cur = con.cursor()

# Create table
# cur.execute('''CREATE TABLE evt1_processCreate(RuleName,UtcTime,ProcessGuid,ProcessId,Image,FileVersion,Description,Product,Company,OriginalFileName,CommandLine,CurrentDirectory,User,LogonGuid,LogonId,TerminalSessionId,IntegrityLevel,Hashes,ParentProcessGuid,ParentProcessId,ParentImage,ParentCommandLine)''')

# cur.execute('''CREATE TABLE evt3_networkConnect(RuleName,UtcTime,ProcessGuid,ProcessId,Image,User,Protocol,Initiated,SourceIsIpv6,SourceIp,SourceHostname,SourcePort,SourcePortName,DestinationIsIpv6,DestinationIp,DestinationHostname,DestinationPort,DestinationPortName)''')

# cur.execute('''CREATE TABLE evt4_sysmonState(UtcTime,State,Version,SchemaVersion)''')

# cur.execute('''CREATE TABLE evt5_processTerminate(RuleName,UtcTime,ProcessGuid,ProcessId,Image)''')

# cur.execute('''CREATE TABLE evt16_sysmonConfigChange(UtcTime,Configuration,ConfigurationFileHash)''')

# cur.execute('''CREATE TABLE evt22_dnsLookup(RuleName,UtcTime,ProcessGuid,ProcessId,QueryName,QueryStatus,QueryResults,Image)''')
# cur.execute('''CREATE TABLE evt11_fileEvent(RuleName,UtcTime,ProcessGuid,ProcessId,imageName,fileName,fileTime)''')
# cur.execute('''CREATE TABLE alertDB(hostname,alert_id,alert_time,alert_details)''')
cur.execute('''CREATE TABLE tConfig(key,value)''')
# cur.execute('''CREATE TABLE openIOC(iocName,iocType,iocDate,iocMitre,iocConditions,status,iocID)''')
# cur.execute('''CREATE TABLE cmdList(hostname,request_time,status,completion_time,result,cmdID)''')

# Insert a row of data
# cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
# con.commit()
# op = cur.execute("""SELECT * FROM alertMon""")
# print(len(op.fetchall()))
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()