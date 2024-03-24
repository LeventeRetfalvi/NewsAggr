import json
import os
from urllib.request import urlopen, urlparse, urlretrieve, urlunparse

import requests
from dotenv import load_dotenv

load_dotenv()


def downloadArticle(url, out_folder):
    filename = url.split("/")[-1]
    if filename == "":
        filename = url.split("/")[-2]
    if not filename.endswith(".html") and not filename.endswith(".htm"):
        filename += ".html"

    outpath = os.path.join(out_folder, filename)
    print(f"path {outpath}")

    urlretrieve(url, outpath)


# downloadArticle(
#    "https://index.hu/belfold/2024/03/20/magyar-peter-volner-schadl-ugy-ugyeszseg-kihallgatas-video/",
#    "d:/NewsAggr",
# )


def downloadFeedly(callback):
    url = "https://api.feedly.com/v3/streams/contents?streamID=user%2Fbca07c1f-bdee-4a93-94d9-258eb580674f%2Fcategory%2Fglobal.all&count=100"
    headers = {
        "Authorization": os.getenv("FEEDLY_TOKEN"),
        "Accept": "application/json",
    }

    r = requests.get(url, headers=headers)
    # print(r.text)

    obj = json.loads(r.text)
    print(obj["id"])
    print(len(obj["items"]))

    for i in obj["items"]:
        try:
            url = i["canonicalUrl"]
        except:
            url = i["alternate"][0]["href"]
        callback(url)


def handleFeedlyItem(url):
    print(url)
    out_folder = os.getenv("TEST_DATA_FOLDER")
    try:
        downloadArticle(url, out_folder)
    except Exception as err:
        print("Unexpected error: ", err)


downloadFeedly(handleFeedlyItem)
