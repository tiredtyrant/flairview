from flask import Flask
from flask import render_template
from flask import g
import sqlite3
import operator

DATABASE = 'flairs.db'

app = Flask(__name__)

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g,'db'):
        g.db.close()

@app.route('/')
def mainpage():
    uflist = {}

    #total de usuarios com flair
    numtotal = g.db.execute('select count(*) from flairs;').fetchone()[0]

    cur = g.db.execute('select distinct uf from flairs;')
    ufs = cur.fetchall()

    for uf in ufs:
        uflist[uf[0]] = g.db.execute('select count(*) from flairs where uf == ?',[uf[0]]).fetchone()[0]
    def getKey(item):
        return item[1]
    return render_template('test.html', var='flair list', uf_list = sorted(uflist.items(),key=getKey,reverse=True), numtotal=numtotal)
    
if __name__ == '__main__':
    app.run(debug=True)