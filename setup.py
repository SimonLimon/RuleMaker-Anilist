import urllib.parse
import requests

redirect_uri = "https://anilist.co/api/v2/oauth/pin"
token_url = 'https://anilist.co/api/v2/oauth/token'


def requestPermission(client_id):
    query_params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code'
    }
    url = 'https://anilist.co/api/v2/oauth/authorize?' + urllib.parse.urlencode(query_params)
    print("Authorization URL:", url)


def codeToAccess(client_id, client_secret):
    authorization_code = input("Put here the code: ")
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': authorization_code
    }
    access_token = ""
    response = requests.post(token_url, data=data, headers={'Accept': 'application/json'})
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        print("Access Token:", access_token)
    else:
        print("Failed to obtain access token:", response.text)
    return access_token
