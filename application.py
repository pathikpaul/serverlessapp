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
USER_POOL_ID = ""
CLIENT_ID = ""

application = Flask(__name__)

PageVisistedCount=0
ssmAPIInvokeUrl=""
IdToken=""
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
             +"</br>"
             +"</br>"
             +"APIInvokeUrl: "+ssmAPIInvokeUrl+" </br>"
             +"</br>"
             +"</br>"
             +"USER_POOL_ID: "+USER_POOL_ID+" </br>"
             +"</br>"
             +"</br>"
             +"CLIENT_ID: "+CLIENT_ID+" </br>"
             +"</br>"
             +"</br>"
             +"IdToken: "+IdToken+"</br>"
             )
    return myString

@application.route('/')
def welcome():
    if  IdToken == "" :
        return redirect(url_for('login'))
    else:
        global notes
        notes=read_notes()
        return render_template("welcome.html",notes=notes)

@application.route('/signout')
def signout():
    global IdToken
    if  IdToken != "" :
        IdToken = ""
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@application.route('/login',methods=["GET","POST"])
def login():
    global IdToken
    if request.method == "GET":
        error = None
        return render_template("login.html", error=error)
    if request.method == "POST":
        if 'LoginButton' in request.form:
            if request.form['email'] == "" or request.form['password'] == "" :
                error = "Please provide both Email and Password"
                return render_template("login.html", error=error)
            username = request.form['email']
            Password = request.form['password']
            client = boto3.client('cognito-idp')
            try:
                resp = client.initiate_auth( ClientId=CLIENT_ID, AuthFlow='USER_PASSWORD_AUTH',
                             AuthParameters={ 'USERNAME': username, 'PASSWORD': Password, },
                             ClientMetadata={ 'username': username, 'password': Password, })
                print('resp: "{}"'.format(json.dumps(resp,indent=2)))
                if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    IdToken=resp["AuthenticationResult"]["IdToken"]
                return redirect(url_for('welcome'))
            except client.exceptions.NotAuthorizedException as e:
                error = e
                return render_template("login.html", error=error)
        if 'ForgotButton' in request.form:
            if request.form['email'] == "" :
               error = "Please provide your Email"
               return render_template("login.html", error=error)
            else:
               client = boto3.client('cognito-idp')
               username = request.form['email']
               resp = client.forgot_password( ClientId=CLIENT_ID, Username=username )
               if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                   return redirect(url_for('confirm_forgot_password', userid=username))
               else:
                   error = None
                   return render_template("login.html", error=error)
        if 'RegisterButton' in request.form:
            if request.form['email'] == "" or request.form['password'] == '' :
               error = "Please provide both Email and Password"
               return render_template("login.html", error=error)
            username = request.form['email']
            Password = request.form['password']
            client = boto3.client('cognito-idp')
            try:
                resp = client.sign_up( ClientId=CLIENT_ID,Username=username, Password=Password)
                print('resp: "{}"'.format(json.dumps(resp,indent=2)))
                if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    print('OK')
                    return redirect(url_for('confirm_sign_up_token', userid=username))
            except client.exceptions.NotAuthorizedException as e:
                error = e
                return render_template("login.html", error=error)

@application.route('/confirm_sign_up_token/<string:userid>',methods=["GET","POST"])
def confirm_sign_up_token(userid):
    if request.method == "GET":
        error = None
        #print ('----------------------------------------')
        #print (userid)
        #print ('----------------------------------------')
        return render_template("confirm_sign_up_token.html", userid=userid, error=error)
    if request.method == "POST":
        if 'BackToLoginScreen' in request.form:
            return redirect(url_for('login'))
        if 'ValidateSignupToken' in request.form:
            if request.form['validationtoken'] == "" :
                error = "Please provide the validation token"
                return render_template("confirm_sign_up_token.html", userid=userid, error=error)
            else:
                client = boto3.client('cognito-idp')
                ConfirmationCode = request.form['validationtoken']
                try:
                    #print("resp = client.confirm_sign_up( ClientId=CLIENT_ID, Username=userid, ConfirmationCode=ConfirmationCode )")
                    resp = client.confirm_sign_up( ClientId=CLIENT_ID, Username=userid, ConfirmationCode=ConfirmationCode )
                    print('resp: "{}"'.format(resp))
                    if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        print('OK')
                        return redirect(url_for('login'))
                except client.exceptions.ExpiredCodeException as e:
                    print("error: {}".format(e))
                    print('ERR')
            return redirect(url_for('login'))
    error = request.form
    return render_template("confirm_sign_up_token.html", userid=userid, error=error)

@application.route('/confirm_forgot_password/<string:userid>',methods=["GET","POST"])
def confirm_forgot_password(userid):
    if request.method == "GET":
        error = None
        #print ('----------------------------------------')
        #print (userid)
        #print ('----------------------------------------')
        return render_template("confirm_forgot_password.html", userid=userid, error=error)
    if request.method == "POST":
        if 'BackToLoginScreen' in request.form:
            return redirect(url_for('login'))
        if 'updatepassword' in request.form:
            if request.form['validationtoken'] == "" or request.form['newpassword'] == "" or request.form['reenterpassword'] == "" :
                error = "Please provide the validation token and both password fields"
                return render_template("confirm_forgot_password.html", userid=userid, error=error)
            if request.form['newpassword'] != request.form['reenterpassword'] :
                error = "Passwords do not match"
                return render_template("confirm_forgot_password.html", userid=userid, error=error)
            else:
                client = boto3.client('cognito-idp')
                ConfirmationCode = request.form['validationtoken']
                try:
                    username = userid
                    ConfirmationCode = request.form['validationtoken']
                    Password=request.form['newpassword']
                    resp = client.confirm_forgot_password( ClientId=CLIENT_ID, Username=username, ConfirmationCode=ConfirmationCode, Password=Password)
                    print('resp: "{}"'.format(resp))
                except client.exceptions.ExpiredCodeException as e:
                    print("error: {}".format(e))
                    print('ERR')
            return redirect(url_for('login'))
    error = request.form
    return render_template("confirm_forgot_password.html", userid=userid, error=error)


@application.route('/note/<int:index>')
def note_view(index):
    try:
        if index<= len(notes)-1:
            return render_template("note.html", note=notes[index],index=index,max_index=len(notes)-1)
        else:
            return redirect(url_for('welcome'))
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
                return redirect(url_for('note_view', index=len(notes)-1))
            else:
                return redirect(url_for('welcome'))
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
    url=ssmAPIInvokeUrl
    headers = {"Content-Type":"application/json",'x-api-key': ssmAPIKeyparameter['Parameter']['Value'],'Authorization': IdToken}
    r=requests.request("GET",url,headers=headers)
    print ("GET: status_code: ",r.status_code)
    print ("GET: text: ",r.text[:100],"...")
    if r.status_code == 200:
        return (json.loads(r.text)['body'])
    else:
        j=[{"topic": "", "comment": ""}]
        return(j)

def write_note(list_of_notes):
    url=ssmAPIInvokeUrl
    headers = {"Content-Type":"application/json",'x-api-key': ssmAPIKeyparameter['Parameter']['Value'],'Authorization': IdToken}
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
ssmAPIInvokeUrl    = ssm.get_parameter(Name='APIInvokeUrl', WithDecryption=True)['Parameter']['Value']
USER_POOL_ID       = ssm.get_parameter(Name='USER_POOL_ID', WithDecryption=True)['Parameter']['Value']
CLIENT_ID          = ssm.get_parameter(Name='CLIENT_ID',    WithDecryption=True)['Parameter']['Value']
ssmAPIKeyparameter = ssm.get_parameter(Name='APIKey',       WithDecryption=True)
#notes=read_notes()

if __name__ == "__main__":
    application.debug = True
    if  len(sys.argv) == 2:
        print("Port To be Used: {0}".format(sys.argv[1]))
        application.run(host='0.0.0.0',port=sys.argv[1])
    else:
        application.run()
