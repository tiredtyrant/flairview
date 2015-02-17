# coding=utf-8

from flask import Flask
from flask import render_template
from flask import g
import sqlite3
import operator

DATABASE = 'flairs.db'

siglas_estados = {'AC':u'Acre', 'AL':u'Alagoas', 'AM':u'Amazonas', 'AP':u'Amapá','BA':u'Bahia','CE':u'Ceará','DF':u'Distrito Federal','ES':u'Espírito Santo','GO':u'Goiás','MA':u'Maranhão','MT':u'Mato Grosso','MS':u'Mato Grosso do Sul','MG':u'Minas Gerais','PA':u'Pará','PB':u'Paraíba','PR':u'Paraná','PE':u'Pernambuco','PI':u'Piauí','RJ':u'Rio de Janeiro','RN':u'Rio Grande do Norte','RO':u'Rondônia','RS':u'Rio Grande do Sul','RR':u'Roraima','SC':u'Santa Catarina','SE':u'Sergipe','SP':u'São Paulo','TO':u'Tocantins','world':u'Outros Países'}
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
		
@app.route('/<uf>')
def showuf(uf):
    userlist = []
    
    users = g.db.execute('select username, cidade from flairs where uf == ?',[uf])
    for user in users:
        userlist.append((user[0],user[1]))
    def getKey(item):
        return item[1]
    return render_template('showuf.html',userlist=sorted(userlist,key=getKey),uf=uf)

@app.route('/')
def mainpage():
    uflist = {}

    #total de usuarios com flair
    numtotal = g.db.execute('select count(*) from flairs;').fetchone()[0]

    cur = g.db.execute('select distinct uf from flairs;')
    ufs = cur.fetchall()

    cur = g.db.execute('select lastdatetime from lastupdate where id == 1;')
    lastupdate = cur.fetchone()[0]

    for uf in ufs:
        uflist[uf[0]] = g.db.execute('select count(*) from flairs where uf == ?',[uf[0]]).fetchone()[0]
    def getKey(item):
        return item[1]
    return render_template('main.html', siglas_estados=siglas_estados, uf_list = sorted(uflist.items(),key=getKey,reverse=True), numtotal=numtotal, lastupdate=lastupdate)
    
if __name__ == '__main__':
    app.run(debug=True)