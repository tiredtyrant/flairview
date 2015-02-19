import praw
import sqlite3
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import uuid

r = praw.Reddit('user-agent')

r.login('user','password')

subreddit = r.get_subreddit('brasil')

def importflairs():
    con = sqlite3.connect('flairs.db')
    cur = con.cursor()
    flair_list = subreddit.get_flair_list(limit=None)
    count = 0
    revisao = str(uuid.uuid4())
    for item in flair_list:
        count += 1
        if cur.execute('SELECT Count(*) FROM flairs WHERE username == ?',(item['user'],)).fetchone()[0]:
            cur.execute('UPDATE flairs SET username=?,uf=?,cidade=?,revisao=? WHERE username==?;',(item['user'],item['flair_css_class'],item['flair_text'],revisao,item['user']))
        else:
            cur.execute('INSERT INTO flairs (uf,username,cidade,revisao) VALUES (?,?,?,?);',(item['flair_css_class'],item['user'],item['flair_text'],revisao))

    cur.execute('DELETE FROM flairs WHERE revisao != ?;',(revisao,))

    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    if cur.execute('SELECT Count(*) FROM lastupdate;').fetchone()[0]:
        cur.execute('UPDATE lastupdate SET id=1,lastdatetime=? WHERE id=1;',(time,))
    else:
        cur.execute('INSERT INTO lastupdate (id, lastdatetime) VALUES (1,?);',(time,))

    con.commit()
    print time
    print count

scheduler = BlockingScheduler()
scheduler.add_job(importflairs, 'interval', hours=3)
try:
    scheduler.start()
except(KeyboardInterrupt,SystemExit):
    pass