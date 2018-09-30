from flask import render_template, flash, redirect, url_for, request ,session
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from .auth import *
from .codechef import *
from app import app
import requests
import requests.auth
import urllib
import os,jsonify , json
from .test_scripts import *
#from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from flask import Response

from datetime import datetime

token = ''

@app.route('/codechef_redirect')
def codechef_redirect():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)

    code = request.args.get('code')

    token = parse_user(code)
    session['token'] = token
    set_user(token)
    print("Got token and user set")
    return redirect(url_for('dashboard'))



@app.route('/index' , methods=['GET', 'POST'])
def dashboard():
    if 'token' not in session:
        return redirect(url_for('login'))
    token = session['token']
    dashboard_data = populate_dashboard(token)
    token_new = client_credentials()
    session['token'] = token_new
    print(token_new)
    contest_details = ongoing_contests(token)
    print(contest_details)
    contest_list = []
    for e in contest_details['result']['data']['content']['contestList']:
        contest_list.append((e['code'], e['endDate']))
        print(e['code'])
        
        
        #continue
    
    
    #for friend
    friends = get_friend_list(session['user'])
    for friend in friends:
        print(friends[friend]) 
    return render_template('index.html', page='IndexPage' , data = dashboard_data , friends=friends , contest_list=contest_list)



@app.route('/' , methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'token' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html', title='Sign in', page="LoginForm" , urlforlogin=make_authorization_url())




@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)



#temporary functions

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('token', None)
   return redirect(url_for('login'))

@app.route('/addFriend', methods=['POST'])
def add_new_fr():
    fname = request.form['fname'] #getting the name from form
    
    db = connectdb()
    #Search / add to database
    
    if search_friend(db,session['user'],fname.lower()):
        print("Friend already there")
        return "UserAF"
    else:


        #searching on codechef
        fdata = get_codechef_user_details(session['token'],fname)
        if fdata['result'].get('data') == None:
            return 'SomeWrong'
        if fdata['result']['data']['message']=='user does not exists':
            return "UserNE"
        fusername = fdata["result"]["data"]["content"]["username"].lower()
        ffullname = fdata["result"]["data"]["content"]["fullname"]
        frating = fdata["result"]["data"]["content"]["ratings"]["allContest"]
        forg = fdata["result"]["data"]["content"]["organization"]
        friend = {'username' : fusername , 'fullname' : ffullname ,'rating' : frating ,'org':forg}
        
        #adding to database
        add_friend(db,session['user'],friend)

        return render_template('_usercard.html' , friend = friend)




#testing area read at your own risk!!

@app.route('/test' , methods=['GET', 'POST'])
def test():
    '''    if 'token' not in session:
        return redirect(url_for('login'))
    token = session['token']
    dashboard_data = populate_dashboard(token)
    token_new = client_credentials()
    print(token_new)    
    print('token printed')'''
    return render_template('test.html', page='TestPage')

@app.route('/update', methods=['POST'])
def update():

    rank = 500

    print('button pressed')
    return Response(json.dumps({'rank' : rank}),  mimetype='application/json')
    