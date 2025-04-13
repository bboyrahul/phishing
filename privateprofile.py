import requests
import json

def get_instagram_profile_pic(username):
    url = f"https://www.instagram.com/{username}/?__a=1&__d=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        try:
            profile_pic_url = data["graphql"]["user"]["profile_pic_url_hd"]
            print(f"Profile Picture URL: {profile_pic_url}")
        except KeyError:
            print("Error: Could not fetch profile picture.")
    else:
        print("Error: Could not access Instagram API. Status Code:", response.status_code)

# Example Usage
username = input("rahul_shots")
get_instagram_profile_pic(username)
