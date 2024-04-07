import requests
import queryList
import setup
import sys

queryUrl = 'https://graphql.anilist.co'

def getUserWatchList(userid, page):
    data = []#list of animes
    variables = {
        'userId': userid,
        'page': page
    }
    response = requests.post(queryUrl, json={'query': queryList.userWatchList, 'variables': variables})
    if response.status_code == 200:
        data = response.json()["data"]["Page"]["mediaList"]
    return data

"""watchList = getUserWatchList(65847, 0)
    for i in watchList:"""

def doSetup(client_id, client_secret):
    setup.requestPermission(client_id)
    access_token = setup.codeToAccess(client_id, client_secret)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = -1
    response = requests.post(queryUrl, headers=headers, json={'query': queryList.userID, 'variables': {}})
    if response.status_code == 200:
        data = response.json()["data"]["Viewer"]["id"]
        print("Your user id is: " + data)
    else:
        print("Failed to obtain id:", response.text)
    sys.exit("Your user id is: " + data + " dont forget to comment the setup lines on main")










