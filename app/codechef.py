from .auth import *
from uuid import uuid4
import requests
import requests.auth
import urllib
import pymongo


CLIENT_ID = "f6b89498de31a8d69507bb20267ea8a4" # Fill this in with your client ID
CLIENT_SECRET = "d689e2bd754200aa479eb60e40e3ca7f" # Fill this in with your client Secret
REDIRECT_URI = "http://localhost:5000/codechef_redirect"



def client_credentials():
    #generate token using client credentials method
    headers = {
    'content-Type': 'application/json',
    }

    data = {
            "grant_type":"client_credentials" ,
            "scope":"public",
            "client_id": CLIENT_ID ,
            "client_secret":CLIENT_SECRET,
            "redirect_uri":REDIRECT_URI
            }
    response = requests.post('https://api.codechef.com/oauth/token', headers=headers, json=data)
    response = response.json()
    print(response)
    print('exec client_cred')
    return response["result"]["data"]["access_token"]

def ongoing_contests(token):
    #get the list of ongoing codechef contests
    token  = client_credentials()
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer '+str(token),
    }

    params = (
        ('status', 'present'),
    )

    response = requests.get('https://api.codechef.com/contests', headers=headers, params=params)
    response = response.json()
    print("djg")
    for i in response["result"]["data"]["content"]["contestList"]:
        print(i["name"])
    return response

def get_todo(token):
    #get the todo list of the logged in user
    headers = {
                'Accept' : 'application/json',
                'Authorization': 'Bearer '+str(token),
                }
    response = requests.get('https://api.codechef.com/todo/problems', headers=headers)
    response = response.json()
    if response["result"]["data"]["code"]!=9001:
        print("ERROR 500")
        redirect(url_for("logout"))
    print(response)
    return response["result"]["data"]

def get_codechef_user(token):
    #get username from codechef to check in database using /users/me query
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+str(token),
    }

    response = requests.get('https://api.codechef.com/users/me', headers=headers)
    response = response.json()

    return response

def get_codechef_user_details(token,user_name):
    #get codechef userdetails of the entered usernames
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+str(token),
    }

    params = (
        ('fields', 'organization,username,rankings,ratings,fullname,username'),
    )

    response = requests.get('https://api.codechef.com/users/'+str(user_name), headers=headers, params=params)
    response = response.json()
    print(response)
    return response

def search_codechef_user_list(token,user_name):
    #search and return list of codechef user_names
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+str(token),
    }

    params = (
        ('search', user_name),
    )

    response = requests.get('https://api.codechef.com/users', headers=headers, params=params)
    response = response.json()
    print(response)
    return response