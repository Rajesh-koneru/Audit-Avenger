from flask import Flask ,redirect,render_template,Blueprint,request,jsonify,session,error
import sqlite3
from flask_login import login_required,LoginManager,UserMixin,login_user
status=Blueprint(__name__,'status')

login_manager = LoginManager()

user_id = request.form.get('id')
# get user by id for login
def get_user_detail(id):
    query="""select auditor_name ,auditor_id from audit_report where auditor_id=id"""
    with sqlite3.connect('auditTracker') as conn:
        pointer = conn.cursor()
        pointer.execute(query)
        data = pointer.fetchone()
        print(data)
        return data
# user model
class User(UserMixin):
    def __int__(self,user_id,username):
        self.user_id=user_id
        self.username=username
    @classmethod
    def get_user_by_id(cls,user_id):
        query1="""select auditor_name, auditor_id from audit_report where auditor_id=id"""
        with sqlite3.connect('auditTracker') as conn:
            pointer = conn.cursor()
            pointer.execute(query1)
            data = pointer.fetchone()
            if data:
                return cls(user_id=data[0], username=data[1])
            return None

# using login manger for seris login
@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)

# auditor verification with there details
@status.route('home/auidtor' ,methods=["POST"])
def auditor_check():
    username=request.form.get('username')
    password=request.form.get('id')
    user_data=get_user_detail(password)
    if user_data:
        if user_data[0]==username and user_data[1]==password:
            user=User(id=user_data[0],username=user_data[1])
            session['username']=username
            session['id']=password
            login_user(user)
            return 'you are authenticated'
@status.route('auditor/update_status')
@login_required
def status_update():
    try:
        query="""select * from audit_report where auditor_id=user_id"""
        with sqlite3.connect('auditTracker') as conn:
            pointer = conn.cursor()
            pointer.execute(query)
            data = pointer.fetchone()
            print(data)
            return jsonify(data)
    except error as e:
        print(e)









