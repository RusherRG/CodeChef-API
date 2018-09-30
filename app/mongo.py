import pymongo
from pymongo import MongoClient


#intitialize settings
db_URI = "mongodb://korusuke:1234567A@ds255768.mlab.com:55768/hackathon"
db = ""

#connecting to the database
def connectdb():
    client = MongoClient(db_URI)
    db = client.hackathon.database
    return db


def updatedb(user_data,username):
    db = connectdb()
    if not check_user(db,username):
        add_user(db,user_data)

    user_dict = update_user(db,user_data)

    return user_dict

def check_user(db,name):
    user_details = db.find_one({"user_details.username":name})

    return user_details


def add_user(db,user):
    usern = user["result"]["data"]["content"]["username"]
    user_dict =  {}
    user_dict["user_details"] = { "fullname" : "","username" : usern,"organization" : "","country" : ""}
    user_dict["rankings"] = {"all": {} ,"long": {},"cookoff": {},"ltime" : {}}
    user_dict["ratings"] = {"all": 0 ,"long": 0,"cookoff": 0,"ltime" : 0}
    user_dict["problemStats"] = {"solved" : {}}
    user_dict["friends"] = {}
    db.insert(user_dict)
    return

def update_user(db,user):
    print(user)
    user_dict =  {}
    user_dict["user_details"] = { "fullname" : "","username" : "","organization" : "","country" : ""}
    user_dict["rankings"] = {"all": {} ,"long": {},"cookoff": {},"ltime" : {}}
    user_dict["ratings"] = {"all": 0 ,"long": 0,"cookoff": 0,"ltime" : 0}
    user_dict["problemStats"] = {"solved": {}}
    

    user = user["result"]["data"]["content"]

    for i in ["username","fullname","organization"]:
        user_dict["user_details"][i] = user[i]

    user_dict["user_details"]["country"] = user["country"]["name"]

    user_dict["rankings"]["all"]["global"],user_dict["rankings"]["all"]["country"] = user["rankings"]["allContestRanking"]["global"],user["rankings"]["allContestRanking"]["country"]
    user_dict["rankings"]["long"]["global"],user_dict["rankings"]["long"]["country"] = user["rankings"]["longRanking"]["global"],user["rankings"]["longRanking"]["country"]
    user_dict["rankings"]["cookoff"]["global"],user_dict["rankings"]["cookoff"]["country"] = user["rankings"]["shortRanking"]["global"],user["rankings"]["shortRanking"]["country"]
    user_dict["rankings"]["ltime"]["global"],user_dict["rankings"]["ltime"]["country"] = user["rankings"]["ltimeRanking"]["global"],user["rankings"]["ltimeRanking"]["country"]

    user_dict["ratings"]["all"] = user["ratings"]["allContest"]
    user_dict["ratings"]["ltime"] = user["ratings"]["lTime"]
    user_dict["ratings"]["cookoff"] = user["ratings"]["short"]
    user_dict["ratings"]["long"] = user["ratings"]["long"]

    for i in user["problemStats"]["solved"].keys():
        user_dict["problemStats"]["solved"][i] = user["problemStats"]["solved"][i]

    print(user["username"])
    db.find_one_and_update({"user_details.username" : user["username"]},
                    {'$set': {"user_details":user_dict["user_details"],"ratings":user_dict["ratings"],"rankings":user_dict["rankings"],"problemStats":user_dict["problemStats"]  }
                    },{'upsert':'true'})

    userp = db.find_one({"user_details.username":"korusuke"})
    print("found korusuke")
    print(userp)
    return user_dict




#friend functions

def get_friend_list(username):
    db = connectdb()
    friend_details = db.find_one({"user_details.username":username})

    return friend_details["friends"]

def search_friend(db,username,fname):
    friend_details = db.find_one({"user_details.username":username})
    print("Searching...")
    return fname.lower() in friend_details["friends"]


def add_friend(db,username,friend):
    #adds the friendname in the database of user
    user = db.find_one({"user_details.username":username})
    user["friends"][friend["username"]] = friend
    db.find_one_and_update({"user_details.username":username},{'$set' : {"friends":user["friends"]}},{'upsert':'true'})
    return 

