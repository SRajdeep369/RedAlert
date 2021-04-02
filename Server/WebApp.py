from flask import Flask, redirect, url_for, jsonify
from flask import request
from flask import render_template
import sqlite3
import datetime
import hashlib
import json



app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/ioc')
def iocPage():
    print("testttt")
    con = sqlite3.connect('RedAlert.db')
    cur = con.cursor()
    cur.execute("""select * from alertMon""")
    rows = cur.fetchall(); 
    con.close()
    print(rows[0][0])
    return render_template('ioc.html',rows=rows)

@app.route('/delIOC',methods=['get'])
def delIOC():
    id = request.args.get('tod')
    id = "'"+id+"'"
    con = sqlite3.connect('RedAlert.db')
    cur = con.cursor()
    cur.execute("delete from alertMon where iocID="+str(id))
    con.commit()
    con.close()
    return redirect(url_for('iocPage'))


@app.route('/addIOC',methods=['POST'])
def addIOC():
    error = None
    if request.method == 'POST':
        print(request.form)
        con = sqlite3.connect('RedAlert.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO alertMon VALUES (?,?,?,?,?,?,?)""",(str(request.form['iocName']),str(request.form['iocType']),str(datetime.datetime.now()),str(request.form['mitreTTP']),str(request.form['iocCon']),str(request.form['iocStatus']),hashlib.md5((str(request.form['iocName'])+str(datetime.datetime.now())).encode()).hexdigest()))
        con.commit()
        con.close()

    return redirect(url_for('iocPage'))

@app.route('/addCMD',methods=['POST'])
def addCMD():
    error = None
    if request.method == 'POST':
        print(request.form)
        con = sqlite3.connect('RedAlert.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO cmdList VALUES (?,?,?,?,?,?,?)""",(str(request.form['hostname']),str(request.form['cmd']),str(datetime.datetime.now()),'pending',"","",hashlib.md5((str(request.form['cmd'])+str(datetime.datetime.now())).encode()).hexdigest()))
        con.commit()
        con.close()

    return redirect(url_for('queueCMD'))

@app.route('/command')
def queueCMD():
    con = sqlite3.connect('RedAlert.db')
    cur = con.cursor()
    cur.execute("""select * from cmdList""")
    rows = cur.fetchall(); 
    print(len(rows))
    lis=[]
    print(lis)
    for i in range(0,len(rows)) :
        lis.append(list(rows[i]))

    for i in range(0,len(lis)) :
        lis[i][5]=lis[i][5].replace("\\\\","\\").replace("\\r","").replace("\\n","<br/>")
        # print(lis[i][5])

    # print(lis)
    con.close()
    return render_template('commands.html',rows=lis)

@app.route('/alerts')
def getAlerts():
    return render_template('alerts.html')
    
@app.route('/iocFinder')
def findIOCs():
    print("testttt")
    con = sqlite3.connect('RedAlert.db')
    cur = con.cursor()
    cur.execute("""select * from searches""")
    rows = cur.fetchall(); 
    con.close()
    print(rows)
    return render_template('iocfinder.html',rows=rows)

    
@app.route('/addSearch',methods=["POST"])
def addSer():
    error = None
    if request.method == 'POST':
        print(request.form)
        con = sqlite3.connect('RedAlert.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO searches VALUES (?,?,?,?,?,?,?)""",(str(request.form['iocName']),str(request.form['iocType']),str(datetime.datetime.now()),str(request.form['mitreTTP']),str(request.form['iocCon']),str(request.form['iocStatus']),hashlib.md5((str(request.form['iocName'])+str(datetime.datetime.now())).encode()).hexdigest()))
        con.commit()
        con.close()

    return redirect(url_for('findIOCs'))

@app.route('/simulate')
def atkSimulation():
    con = sqlite3.connect('RedAlert.db')
    cur = con.cursor()
    cur.execute("""select * from aptGrp""")
    rows = cur.fetchall(); 
    con.close()
    print(rows[0][0])
    return render_template('simulate.html',rows=rows)


@app.route('/addSim',methods=["POST"])
def addSim():
    if request.method == 'POST':
        print(request.form)
        con = sqlite3.connect('RedAlert.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO aptGrp VALUES (?,?,?,?,?)""",(str(request.form['grpName']),hashlib.md5((str(request.form['grpName'])+str(datetime.datetime.now())).encode()).hexdigest(),str(request.form['ttpLST']),str(request.form['Status']),str(request.form['grpdesc'])))
        con.commit()
        con.close()

    return redirect(url_for('atkSimulation'))


@app.route('/getCommands',methods=['GET','POST'])
def getCmds():
    if request.method == 'GET':
        hst = request.args.get('hostname')
        con = sqlite3.connect('RedAlert.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        rows = cur.execute("SELECT * from cmdList where hostname="+"'"+str(hst)+"' and status='pending'").fetchall()
        con.commit()
        con.close()
        return json.dumps( [dict(ix) for ix in rows] )
    if request.method == 'POST':
        print("Hellooooo")
        for cid,resp in request.json.items():
            # print(str(cid)+" : "+resp)
            con = sqlite3.connect('RedAlert.db')
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            rows = cur.execute("update cmdList set status='Complete', result='"+resp+"',completion_time='"+str(datetime.datetime.now())+"' where cmdID='"+cid+"'")
            con.commit()
            con.close()
            print("----------------------------")
        return "Success"

if __name__ == '__main__':
    app.run()