
from flask import Flask, Response, request, render_template, url_for, redirect
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import urllib2
import json
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
    return "logout successfull"
@app.route("/")
@login_required
def index():
    return render_template("dashboard.html")

@app.route("/upload")
@login_required
def upload():
    return render_template("upload.html", value=current_user.id)

@app.route("/create")
@login_required
def create():
    return render_template("create.html", value=current_user.id)
if __name__ == '__main__':
    print urllib2.urlopen(SERVER_ADDRESS+"api/getUser/1").read()

    app.config["SECRET_KEY"] = "ITSASECRET"
    app.run(port=4999,debug=True)