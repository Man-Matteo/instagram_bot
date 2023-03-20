import requests
import json

# I get the access token (how???) and userID of the authenticated user

# I get a short-lived access token, then with an API call I convert it into a long-lived token (60 days)
# i get the user id with https://graph.instagram.com/me?fields=id&access_token=<access_token> replacing <access token> with the token i got



# uload photo
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
