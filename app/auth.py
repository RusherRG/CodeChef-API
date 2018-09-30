#!/usr/bin/env python
from flask import Flask, abort, request
from uuid import uuid4
import requests
import requests.auth
import urllib
import pymongo
from .mongo import *
from .dashboard import *

CLIENT_ID = "f6b89498de31a8d69507bb20267ea8a4" # Fill this in with your client ID
CLIENT_SECRET = "d689e2bd754200aa479eb60e40e3ca7f" # Fill this in with your client Secret
REDIRECT_URI = "http://localhost:5000/codechef_redirect"




def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    state = str(uuid4())
    save_created_state(state)
    params = {"response_type": "code",
              "client_id": CLIENT_ID,
              "state": state, 
              "redirect_uri": REDIRECT_URI,
              }
    url = "https://api.codechef.com/oauth/authorize?" + urllib.parse.urlencode(params)
    return url


# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache.
def save_created_state(state):
    pass
def is_valid_state(state):
    return True




def get_token(code):
	head = {
    			'content-Type': 'application/json',
		  }
	data = { "grant_type": "authorization_code",
		  "code": code,
		  "client_id": CLIENT_ID,
		  "client_secret": CLIENT_SECRET,
		  "redirect_uri":REDIRECT_URI,
		}
	
	response = requests.post('https://api.codechef.com/oauth/token' ,  json=data)
	response = response.json()
	print(response)
	print("Token Response Recieved")
	return response["result"]["data"]["access_token"]



def parse_user(code):
	token = get_token(code)
	return token

def get_user_me(acode):
	headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+acode,
}

	response = requests.get('https://api.codechef.com/users/me', headers=headers)
	response = response.json()

	return response
