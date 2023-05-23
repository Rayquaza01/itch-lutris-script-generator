import requests
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("url", help="The URL of the game from itch.io")
ap.add_argument("--api-key", help="The API key for your account")
args = ap.parse_args()

itchpage = requests.get(args.url + "/data.json").json()
print(itchpage["id"])

# TODO
# https://github.com/lutris/lutris/blob/27905d75b99bcb6cdaeef0d9a6dd5c388ed1a73e/lutris/services/itchio.py#L309
