
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

@app.route("/viewexp/<int:experiment_id>",methods = ['GET', 'POST'])
@login_required
def viewexp1(experiment_id):
    jsonString  = urllib2.urlopen(SERVER_ADDRESS+"api/" + "toggleExperiment/" + str(experiment_id)).read()
    return redirect(url_for("viewexp"))

@app.route("/create",methods = ['GET', 'POST'])
@login_required
def create():
    if request.method == "GET":
        jsonString  = urllib2.urlopen(SERVER_ADDRESS+"api/" + str(current_user.id) + "/datasets").read()
        if(len(jsonString)<=0):
            return None
        jsonArr = json.loads(jsonString)
        if(jsonArr['status'] == 200):
            return render_template("create.html", value = str(current_user.id), data = jsonArr)
    if(len(request.form) > 0):
        argArray = request.form
    else:
        return "ee"
        print request.get_data()
        argArray = json.loads(request.data)
    values = {'dataset_id' : argArray.get("dataset_id"),
              'batchSize' : argArray.get("batchSize"),
              'price' : argArray.get("price") ,
              'description' : argArray.get("description"),
              'gender' :  argArray.get("gender"),
			  'title' : argArray.get('title'),
				'maxTime' : argArray.get('maxTime'),
				'allocateTime': argArray.get('allocateTime'),
				'notifTime' : argArray.get('notifTime'),
				'datasetType' : argArray.get('datasetType'),
				'skill' : argArray.get('skill'),
				'country' : argArray.get('country')
			 }

    data=urllib.urlencode(values)
    print str(data)
    data=data.encode('utf-8')
    response=urllib.urlopen(SERVER_ADDRESS+"api/" + str(current_user.id) + "/create",data)
    jsonString=response.read()
    #data = data.encode('ascii') # data should be bytes
    #jsonString = urllib2.urlopen(SERVER_ADDRESS+"api/" + str(current_user.id) + "/create", data).read()
    #jsonString = urllib.request.urlopen(req).read()
    print jsonString
    jsonArr = json.loads(jsonString)
    if(jsonArr['status'] == 200):
        jsonString  = urllib2.urlopen(SERVER_ADDRESS+"api/" + str(current_user.id) + "/datasets").read()
        jsonArr2 = json.loads(jsonString)
        return render_template("create.html", value = str(current_user.id), succ = jsonArr, data=jsonArr2)
    else:
        jsonString  = urllib2.urlopen(SERVER_ADDRESS+"api/" + str(current_user.id) + "/datasets").read()
        jsonArr2 = json.loads(jsonString)
        if(jsonArr2['status'] == 200):
            return render_template("create.html", value = str(current_user.id), data = jsonArr2, fail=jsonArr)
        return render_template("create.html", value = str(current_user.id), fail = jsonArr, data={})

@app.route("/rateBatch/<int:experiment_id>",methods = ['GET', 'POST'])
@login_required
def rateBatch(experiment_id):
    if request.method == "GET":
        jsonString  = urllib2.urlopen(SERVER_ADDRESS+"api/" + "getBatchToRate/" + str(experiment_id)).read()
        if(len(jsonString)<=0):
            return None
        jsonArr = json.loads(jsonString)
        if(jsonArr['status'] == 200):
            return render_template("rateBatch.html", data = jsonArr, id = str(experiment_id), flag = 0)
    if(len(request.form) > 0):
        argArray = request.form
    else:
        print request.get_data()
        argArray = json.loads(request.data)
    values = {
        'batch_id': argArray.get('batch_id'),
        'rating': argArray.get('rating')
    }
    data=urllib.urlencode(values)
    print str(data)
    data=data.encode('utf-8')
    response=urllib.urlopen(SERVER_ADDRESS+"api/" + values['batch_id'] + "/rateBatch/" +  values['batch_id'],data)
    jsonString=response.read()
    print jsonString
    jsonArr = json.loads(jsonString)
    if(jsonArr['status'] == 200):
        jsonString  = urllib2.urlopen(SERVER_ADDRESS+"api/" + "getBatchToRate/" + str(experiment_id)).read()
        jsonArr = json.loads(jsonString)
        if(jsonArr['status'] == 200):
            return render_template("rateBatch.html", data = jsonArr, id = str(experiment_id))
    else:
        return "ee"

@app.route("/updateExp/<int:experiment_id>",methods = ['GET', 'POST'])
@login_required
def updateExp(experiment_id):
    if request.method == "GET":
        jsonString  = urllib2.urlopen(SERVER_ADDRESS+"api/" + "getExperimentDetails/" + str(experiment_id)).read()
        if(len(jsonString)<=0):
            return None
        jsonArr = json.loads(jsonString)
        if(jsonArr['status'] == 200):
            return render_template("updateExp.html", data = jsonArr, id = str(experiment_id))
    if(len(request.form) > 0):
        argArray = request.form
    else:
        print request.get_data()
        argArray = json.loads(request.data)
    values = {
        'allocateTime': argArray.get('allocateTime'),
        'description': argArray.get('description'),
        'maxTime': argArray.get('maxTime'),
        'notifTime': argArray.get('notifTime')
    }
    print "jj"+argArray.get('allocateTime') + "h\n"
    data=urllib.urlencode(values)
    #print str(data)
    data=data.encode('utf-8')
    response=urllib.urlopen(SERVER_ADDRESS+"api/" + "updateExperiment/" + str(experiment_id),data)
    jsonString=response.read()
    print jsonString
    jsonArr = json.loads(jsonString)
    if(jsonArr['status'] == 200):
        jsonString2  = urllib2.urlopen(SERVER_ADDRESS+"api/" + "getExperimentDetails/" + str(experiment_id)).read()
        jsonArr = json.loads(jsonString2)
        if(jsonArr['status'] == 200):
            return render_template("updateExp.html", data = jsonArr, id = str(experiment_id), flag = 1)
    else:
        return render_template("updateExp.html", data = jsonArr, id = str(experiment_id), flag = 2)

if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSASECRET"
    app.run(port=4999,debug=True,host="0.0.0.0")
