import praw
import sqlite3

r = praw.Reddit('user-agent')

r.login('user','password')

subreddit = r.get_subreddit('brasil')

con = sqlite3.connect('flairs.db')
cur = con.cursor()

flair_list = subreddit.get_flair_list(limit=None)
count = 0
for item in flair_list:
    count += 1
    print item
    cur.execute('INSERT INTO flairs (uf,username,cidade) VALUES (\'%s\',\'%s\',\'%s\');'%(item['flair_css_class'].encode('utf-8'),item['user'].encode('utf-8'),item['flair_text'].encode('utf-8')))

con.commit()
print count