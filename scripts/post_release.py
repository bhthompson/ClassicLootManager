from discord import Webhook, RequestsWebhookAdapter, Embed
import requests
import time
import sys

if len(sys.argv) != 2:
    print("Invalid arguments")
    exit(1)

GIT_ENDPOINT = "https://api.github.com/repos/lantisnt/classiclootmanager/releases"

def get_newest_release():
    num_calls = 0
    while True:
        num_calls = num_calls + 1
        response = requests.get(GIT_ENDPOINT)
        if response.status_code == 200:
            return response.json()
        else:
            print("Query failed")
            if num_calls >= 10:
                print("Exiting")
                exit(10)
            else:
                print("Sleeping and retrying")
                time.sleep(num_calls)

releases = get_newest_release()

if len(releases) == 0:
    print("No releases found")
    exit(20)

try:
    body = releases[0]["body"]
    tag = releases[0]["tag_name"]
    prerelease = releases[0]["prerelease"]

    embed = {
        "author": {"name": tag},
        "title": "New version of Classic Loot Manager has just been released!",
        "color": 14464841,
        "fields": [
            {"name": "**CHANGELOG**", "value": "```" + body + "```", "inline": False}
        ]
    }

    if prerelease:
        embed["description"] = "_This is a beta version and may still contain bugs_"

    webhook = Webhook.from_url(sys.argv[1], adapter = RequestsWebhookAdapter())
    webhook.send(embed = Embed.from_dict(embed))
except Exception as e:
    print(str(e))
    exit(30)