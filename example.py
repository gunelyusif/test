#!/usr/bin/

from rlcompleter import get_class_members
import urllib2
import urllib
import json
import MySQLdb as mdb
from MySQLdb.cursors import DictCursor
from flask import Flask,render_template,request
app = Flask(__name__)
from pprint import pprint
con = mdb.connect(host='127.0.0.1',user='root', passwd='',use_unicode=True,db='test',cursorclass=DictCursor);

con.set_character_set('utf8')
cur = con.cursor()
#cur.execute("insert")


@app.route('/liste', methods=['GET','POST'])
def KayitListesi():
    if (request.method=="POST"):
        like="WHERE olay LIKE '%"+request.form['search']+"%'"
    else:
        like=""

    sorgu="SELECT * FROM Proje "+like;


    cur.execute(sorgu)
    donenKayitlar=cur.fetchall()
    return render_template("proje.html",kayitlar=donenKayitlar).encode('utf-8')


@app.route('/proje',methods=['GET'])
def Proje():
    month =["Ocak","%C5%9Eubat","Mart","Nisan","May%C4%B1s","Haziran","Temmuz","A%C4%9Fustos","Eyl%C3%BCl","Ekim","Kas%C4%B1m","Aral%C4%B1k"]
    for item in month:
        for day in range (1,31):
             req = urllib2.urlopen("http://tr.wikipedia.org/w/api.php?format=json&action=query&titles="+str(day)+"+"+item+"&page=1&prop=revisions&rvprop=content")
             content = req.read()
             d = json.loads(content)
             key=d['query']['pages'].keys()[0]
             try:
                olaylar=d['query']['pages'][key]['revisions'][0]["*"].split("== Olaylar ==")[1].split("== Do0xc4umlar ==")[0].split("*")
             except:
                 olaylar=[]
             for olay in olaylar:
                 print olay
                 olay=olay.replace("[","")
                 olay=olay.replace("]","")
                 olay=olay.replace("}","")
                 olay=olay.replace("{","")

                #cur.execute("SELECT * FROM `Proje` ")
                 insertSQL='INSERT INTO Proje (Gun,Ay,Olay) VALUES ("%s","%s","%s")' %(str(day),item,mdb.escape_string(olay.encode('utf-8')))
                 cur.execute(insertSQL)
                 con.commit()

    return render_template("proje.html")

app.run()




