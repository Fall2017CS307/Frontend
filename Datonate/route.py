
from flask import Flask, Response, request, render_template, url_for, redirect
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import urllib2
import urllib
#import urllib.request
import json
import requests
from urlparse import urlparse

SERVER_ADDRESS = "http://datonate.com:5000/"

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

def getUser(id):
    jsonString  = urllib2.urlopen(SERVER_ADDRESS+"api/getUser/" + str(id)).read()
    if(len(jsonString)<=0):
        return None
    jsonArr = json.loads(jsonString)
    return User(jsonArr['id'], jsonArr['name'])

class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name= name

@login_manager.user_loader
def load_user(user_id):
    return getUser(user_id)

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "GET":
        argArray = request.args
    elif request.method  == "POST":
        if(len(request.form) > 0):
            argArray = request.form
        else:
            print request.get_data()
            argArray = json.loads(request.data)

    username = argArray.get("email")
    password = argArray.get("password")
    if(username is None or password is None or len(username) < 1 or len(password) < 1 ):
        return render_template("index.html")
    jsonString  = urllib2.urlopen(SERVER_ADDRESS+"api/login?email="+username+"&password="+password).read()
    jsonArr = json.loads(jsonString)
    if(jsonArr['status']!=200):
        return render_template("index.html")

    usr = getUser(jsonArr['id'])
    login_user(usr)

    return redirect(url_for("index"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
@app.route("/")
@login_required
def index():
    return render_template("dashboard.html")

@app.route("/upload")
@login_required
def upload():
    return render_template("upload.html", value=current_user.id)

@app.route("/viewdataset")
@login_required
def viewdataset():
    jsonString  = urllib2.urlopen(SERVER_ADDRESS+"api/" + str(current_user.id) + "/datasets").read()
    if(len(jsonString)<=0):
        return None
    jsonArr = json.loads(jsonString)
    if(jsonArr['status'] == 200):
        return render_template("viewdataset.html", value=jsonArr)

@app.route("/viewexp")
@login_required
def viewexp():
    jsonString  = urllib2.urlopen(SERVER_ADDRESS+"api/" + "getExperimentProgress/" + str(current_user.id)).read()
    if(len(jsonString)<=0):
        return None
    jsonArr = json.loads(jsonString)
    if(jsonArr['status'] == 200):
        return render_template("viewexp.html", value=jsonArr)

@app.route("/create")
@login_required
def create():
    if request.method == "GET":
        argArray = request.args
    elif request.method  == "POST":
        if(len(request.form) > 0):
            argArray = request.form
        else:
            print request.get_data()
            argArray = json.loads(request.data)
    values = {'dataset_id' : argArray.get("dataset_id"),
              'batchSize' : argArray.get("batchSize"),
              'price' : argArray.get("price") ,
              'description' : argArray.get("description"),
              'gender' :  argArray.get("gender") }
    data=urllib.urlencode(values)
    data=data.encode('utf-8')
    response=urllib.urlopen(SERVER_ADDRESS+"api/" + str(current_user.id) + "/create",data)
    jsonString=response.read()
    #data = data.encode('ascii') # data should be bytes
    #jsonString = urllib2.urlopen(SERVER_ADDRESS+"api/" + str(current_user.id) + "/create", data).read()
    #jsonString = urllib.request.urlopen(req).read()
    jsonArr = json.loads(jsonString)
    if(jsonArr['status'] == 200):
        return render_template("create.html", value = str(current_user.id), succ = jsonArr)
    else:
        return render_template("create.html", value = str(current_user.id), fail = jsonArr)

if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSASECRET"
    app.run(port=5000,debug=True,host="0.0.0.0")
