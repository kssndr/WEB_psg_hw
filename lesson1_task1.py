import requests
import json

main_api_link = "https://api.github.com/users/"
user = "ilyaKhim"
get_repos = "repos"

req = requests.get(f"{main_api_link}{user}/{get_repos}")

if req.ok:
    with open(f'user_{user}_repos_.json', 'wb') as file:
        file.write(req.content)
