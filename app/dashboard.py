import requests
import requests.auth
import urllib
from flask import render_template, flash, redirect, url_for, request ,session
from .codechef import *
from .mongo import *

def populate_dashboard(token):
    #all function calls that uses same dictionary
    user_dict = session['user_dict']
    #todo = get_todo(token)
    #contests =  ongoing_contests()
    return user_dict

def set_user(token):
    #to be run only once when redirecting

    user_data = get_codechef_user(token)
    username = user_data["result"]["data"]["content"]["username"]

    session['user'] = username

    user_dict = updatedb(user_data,username)
    print("updated")
    print(user_dict)
    session['user_dict'] = user_dict

    return