#########################################
##    bento/centos-7.2  (came with Python 2.7.5 installed)
#########################################
##    sudo yum install python-virtualenv
##    mkdir myproject
##    cd myproject
##    python2 -m virtualenv venv
##    cd /home/hadoop/myproject
##    . venv/bin/activate
##    pip install Flask==1.1.2
##    vi myfirstapp.py
##    export  FLASK_ENV=development
##    export  FLASK_APP=myfirstapp
##    flask run 
##    flask run --host=192.168.77.10
#########################################
import json
import flask
import platform
import socket
import requests
from datetime import datetime
from flask import Flask,render_template,request,abort,redirect,url_for
import os.path
import sys
import boto3

application = Flask(__name__)

PageVisistedCount=0
@application.route('/info')
def info():
    global PageVisistedCount
    PageVisistedCount=PageVisistedCount+1
    FlaskVersion=flask.__version__
    myhostname = socket.gethostname()
    #myip_address = socket.gethostbyname(myhostname)
    myString=("Hello, World!"+"</br>"
             +"FlaskVersion="+FlaskVersion+"</br>"
             +"Running At: "+str(datetime.now())+"</br>"
             +"OS: "+str(platform.platform())+"</br>"
             +"Release: "+str(platform.linux_distribution())+"</br>"
             +"Hostname: "+myhostname+"</br>"
             +"</br>"
             +"</br>"
             +"PageVisisted: "+str(PageVisistedCount)+" times</br>"
             )
    return myString

@application.route('/')
def welcome():
   return render_template("welcome.html",notes=notes)

@application.route('/note/<int:index>')
def note_view(index):
    try:
        if index<= len(notes)-1:
            return render_template("note.html", note=notes[index],index=index,max_index=len(notes)-1)
        else:
            return render_template("welcome.html",notes=notes)
    except IndexError:
        abort(404)

@application.route('/delete_note/<int:index>',methods=["GET","POST"])
def delete_note(index):
    if request.method == "GET":
        if index<= len(notes)-1:
            return render_template("delete_note.html",note=notes[index],index=index)
        else:
            return render_template("welcome.html",notes=notes)
    if request.method == "POST":
        try:
            notes.pop(index)
            write_note(notes)
            if index<= len(notes)-1:
                return render_template("note.html", note=notes[index],index=index,max_index=len(notes)-1)
            else:
                return render_template("welcome.html",notes=notes)
        except IndexError:
            abort(404)
@application.route('/add_note',methods=["GET","POST"])
def add_note():
    if request.method == "GET":
        return render_template("add_note.html")
    if request.method == "POST":
        note={'topic': request.form["topic"], 'comment': request.form["comment"]}
        notes.append(note)
        write_note(notes)
        return redirect(url_for('note_view', index=len(notes)-1))

def read_notes():
    url="https://ajsgokslc5.execute-api.us-west-2.amazonaws.com/dev/"
    headers = {'x-api-key': ssmAPIKeyparameter['Parameter']['Value']}
    r=requests.request("GET",url,headers=headers)
    print ("GET: status_code: ",r.status_code)
    print ("GET: text: ",r.text[:100],"...")
    if r.status_code == 200:
        return (json.loads(r.text)['body'])
    else:
        j=[{"topic": "", "comment": ""}]
        return(j)

def write_note(list_of_notes):
    url="https://ajsgokslc5.execute-api.us-west-2.amazonaws.com/dev/"
    headers = {"Content-Type":"application/json",'x-api-key': ssmAPIKeyparameter['Parameter']['Value']}
    data='{ "list_of_notes": '+json.dumps(list_of_notes)+' }'
    r=requests.request("POST",url,headers=headers,data=data)
    print ("POST: status_code: ",r.status_code)
    print ("POST: text: ",r.text[:100],"...")
    if r.status_code == 200:
        return (json.loads(r.text)['body'])
    else:
        print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
        print('Response code: %d\n' % r.status_code)
        print("Type: ",type(r.text))
        print(r.text)
        j=[{"topic": "", "comment": ""}]
        return(j)

ssm = boto3.client('ssm')
ssmAPIKeyparameter = ssm.get_parameter(Name='APIKey', WithDecryption=True)
notes=read_notes()

if __name__ == "__main__":
    application.debug = True
    if  len(sys.argv) == 2:
        print("Port To be Used: {0}".format(sys.argv[1]))
        application.run(host='0.0.0.0',port=sys.argv[1])
    else:
        application.run()
