from bs4 import BeautifulSoup
import requests
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("url", help="The URL of the game from itch.io")
args = ap.parse_args()

itchpage = requests.get(args.url).content

parser = BeautifulSoup(itchpage, "html.parser")
id = parser.select_one('meta[name="itch:path"]').get("content").split("/")[1]
print(id)
