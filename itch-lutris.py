#!/usr/bin/env python3
import json
import urllib.request
import subprocess
import argparse
import re
import os

# from https://github.com/lutris/lutris/blob/27905d75b99bcb6cdaeef0d9a6dd5c388ed1a73e/lutris/installer/__init__.py#L10
AUTO_EXE_PREFIX = "_xXx_AUTO_"
AUTO_ELF_EXE = AUTO_EXE_PREFIX + "ELF_xXx_"
AUTO_WIN32_EXE = AUTO_EXE_PREFIX + "WIN32_xXx_"


# generate a slug for the game by replacing spaces with dashes, changing to lowecase, and removing special chars
# might not be perfect, but it seems to get the job done in most cases.
def generateSlug(name):
    return re.sub("[^a-zA-Z0-9\-_]", "", name.lower().replace(" ", "-"))

# script generation largely based on
# https://github.com/lutris/lutris/blob/27905d75b99bcb6cdaeef0d9a6dd5c388ed1a73e/lutris/services/itchio.py#L309
def generateInstaller(name, id, runner):
    if (runner == "linux"):
        game_config = {"exe": AUTO_ELF_EXE}
        script = [
            {"extract": {"file": "itchupload", "dst": "$CACHE"}},
            {"merge": {"src": "$CACHE", "dst": "$GAMEDIR"}},
        ]
    elif (runner == "wine"):
        game_config = {"exe": AUTO_WIN32_EXE}
        script = [
            {"task": {"name": "create_prefix"}},
            {"install_or_extract": "itchupload"}
        ]

    return {
        "name": name,
        "version": "itch.io",
        "slug": generateSlug(name),
        "game_slug": generateSlug(name),
        "runner": runner,
        "itchid": id,
        "script": {
            "files": [
                {"itchupload": "N/A:Select the installer from itch.io"}
            ],
            "game": game_config,
            "installer": script,
        }
    }

ap = argparse.ArgumentParser()
ap.add_argument("url", help="The URL of the game from itch.io")
ap.add_argument("--api-key", help="The API key for your account. Optional if force linux or force wine is set")
ap.add_argument("-l", "--force-linux", help="Forces the installer to use linux. Optional if apikey is set", action="store_true")
ap.add_argument("-w", "--force-wine", help="Forces the installer to use wine. Optional if apikey is set", action="store_true")
ap.add_argument("-i", "--install", help="Launches lutris to install the script immediately", action="store_true")
args = ap.parse_args()

itchpage = json.loads(urllib.request.urlopen(args.url + "/data.json").read().decode("utf-8"))

id = str(itchpage["id"])
name = itchpage["title"]
print("Checking versions of " + id + " " + name)

# if no api key, don't make request
if args.api_key:
    # this request might be better done using the https://api.itch.io/games/<id> endpoint
    # however, this endpoint *also* requires authentication, so an API key is still needed.
    # leaving it like this because both basically do the same thing
    uploads = json.loads(urllib.request.urlopen("https://itch.io/api/1/" + args.api_key + "/game/" + id + "/uploads").read().decode("utf-8"))
else:
    uploads = { "uploads": []}

# generate various installers
# if force linux or force wine is set, force those versions
# if not set, dynamically detect the version to use based on the itch api
# try linux first, then wine if no linux, then fail if neither
if args.force_linux:
    script = generateInstaller(name, id, "linux")
elif args.force_wine:
    script = generateInstaller(name, id, "wine")
elif any(i["p_linux"] for i in uploads["uploads"]):
    script = generateInstaller(name, id, "linux")
elif any(i["p_windows"] for i in uploads["uploads"]):
    script = generateInstaller(name, id, "wine")
else:
    # no installable versions
    print("No installable versions!")
    if not args.api_key:
        print("You need to have an apikey to automatically detect what version to use")
        print("You can get one here: https://itch.io/user/settings/api-keys")
        print("Otherwise, you can force a specific version using the --force-linux or --force-wine flags")
    exit()

filename = generateSlug(name) + ".json"

with open(filename, "w") as f:
    f.write(json.dumps(script))

print("Script written to " + generateSlug(name) + ".json")

if args.install:
    print("Installing with lutris")
    subprocess.Popen(["lutris", "-i", os.path.join(os.getcwd(), filename)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
