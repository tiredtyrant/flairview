import praw
import sqlite3
import datetime

r = praw.Reddit('user-agent')

r.login('user','password')

subreddit = r.get_subreddit('brasil')

con = sqlite3.connect('flairs.db')
cur = con.cursor()

flair_list = subreddit.get_flair_list(limit=None)
count = 0
for item in flair_list:
    count += 1
    cur.execute('INSERT INTO flairs (uf,username,cidade) VALUES (?,?,?);',(item['flair_css_class'],item['user'],item['flair_text']))

time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
if cur.execute('select Count(*) from lastupdate;').fetchone()[0]:
    cur.execute('UPDATE lastupdate SET id=1,lastdatetime=? WHERE id=1;',(time,))
else:
    cur.execute('INSERT INTO lastupdate (id, lastdatetime) VALUES (1,?);',(time,))

con.commit()
print time
print count