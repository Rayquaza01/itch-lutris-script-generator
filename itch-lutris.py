import requests
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("url", help="The URL of the game from itch.io")
ap.add_argument("--api-key", help="The API key for your account")
args = ap.parse_args()

itchpage = requests.get(args.url + "/data.json").json()

id = str(itchpage["id"])
name = itchpage["title"]
print(id + " " + name)

uploads = requests.get("https://itch.io/api/1/" + args.api_key + "/game/" + id + "/uploads").json()

linux = [i for i in uploads["uploads"] if i["p_linux"]]
if len(linux) > 0:
    print(linux[0])
else:
    windows = [i for i in uploads["uploads"] if i["p_windows"]]
    if (len(windows) > 0):
        print(windows[0])
    else:
        # no versions available
        exit()

# TODO
# https://github.com/lutris/lutris/blob/27905d75b99bcb6cdaeef0d9a6dd5c388ed1a73e/lutris/services/itchio.py#L309
