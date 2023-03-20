import requests
import json
from flask import Flask, request
#obtaining access token

app = Flask(__name__)
@app.route('/instagram/callback/')
def handle_callback():
    # Step 1: Authentication
    client_id = 'YOUR CLIENT ID'
    redirect_uri = 'YOUR CALLBACK URL'
    auth_url = f'https://api.instagram.com/oauth/authorize/?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
    print(f'Visit this URL and authorize your application: {auth_url}')

    # Step 2: Redirection
    code = input('Insert temporary authorization code: ')

    # Step 3: Token exchange
    client_secret = 'YOUR CLIENT SECRET KEY'
    access_token_url = 'https://api.instagram.com/oauth/access_token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': code
    }
    response = requests.post(access_token_url, data=payload)

    # Step 4: Obtaining access token
    access_token = response.json()['access_token']
    print(f'Valid access token: {access_token}')
    
    return 'Authorization success!'

if __name__ == '__main__':
app.run(port=8000)

# user-id
username = "matteomannai3"
user-id = f"https://api.instagram.com/v1/users/search?q={username}&access_token={access_token}"

# upload photo
file_path = r"C:\Users\hp\Desktop\bot\image.jpg"
url = f"https://graph.instagram.com/{user-id}/media"
params = {"access_token": "your-access-token"}
files = {"file": open(f"{file_path}", "rb")}
response = requests.post(url, params=params, files=files)

# add description
media_id = response.json()["id"]
url = f"https://graph.instagram.com/{media_id}"
params = {"access_token": "your-access-token", "caption": "Replace with photo description"}
response = requests.post(url, params=params)

# publish photo
url = f"https://graph.instagram.com/{user-id}/media/{media_id}/?access_token=your-access-token&action=publish"
response = requests.post(url)

# check response status
if response.status_code == 200:
    print("Success!")
else:
    print(f"Error {response.status_code}: {response.text}")
