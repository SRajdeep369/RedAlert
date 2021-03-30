from flask import Flask, redirect, url_for
from flask import request
from flask import render_template
import sqlite3
import datetime
import hashlib



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
    con.close()
    return render_template('commands.html',rows=rows)

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
    return render_template('simulate.html')

if __name__ == '__main__':
    app.run()