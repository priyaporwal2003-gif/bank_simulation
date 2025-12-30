import sqlite3

def create():
    conobj=sqlite3.connect(database='mybank.sqlite')
    curobj=conobj.cursor()
    query='''
create table if not exists accounts(
acn integer primary key autoincrement,
name text,
pass text,
mob text,
email text,
adhar text,
bal float,
opendate datetime
)
''' 

    curobj.execute(query)
    conobj.close()
