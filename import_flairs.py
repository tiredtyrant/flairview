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
    query = 'INSERT INTO flairs (uf,username,cidade) VALUES (\'%s\',\'%s\',\'%s\');'%(item['flair_css_class'],item['user'],item['flair_text'])
    cur.execute(query)

con.commit()
print count