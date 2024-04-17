import json
import os
from urllib.request import urlopen, urlparse, urlretrieve, urlunparse

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

CSV_FILE_NAME = "data.csv"
CSV_COLUMN_URL = "Url"
CSV_COLUMN_PATH = "Path"

CSV_COLUMN_DEFINITION = {
    CSV_COLUMN_URL: [],
    CSV_COLUMN_PATH: [],
    "Any number": [],
    "Any string": [],
}


def downloadArticle(url, out_folder):
    filename = url.split("/")[-1]
    if filename == "":
        filename = url.split("/")[-2]
    if not filename.endswith(".html") and not filename.endswith(".htm"):
        filename += ".html"

    outpath = os.path.join(out_folder, filename)
    print(f"path {outpath}")

    urlretrieve(url, outpath)
    return outpath


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

    obj = json.loads(r.text)
    if r.status_code != 200:
        raise Exception(
            "Cannot dowload Feedly: {errorMessage}.".format(
                errorMessage=obj["errorMessage"]
            )
        )

    # print(obj)
    # print(obj["id"])
    # print(len(obj["items"]))

    for i in obj["items"]:
        try:
            url = i["canonicalUrl"]
        except Exception:
            url = i["alternate"][0]["href"]
        callback(url)


def handleFeedlyItem(url):
    global duplicates
    global newArticles
    global errors

    print(url)
    out_folder = os.getenv("TEST_DATA_FOLDER")
    try:
        for i in df.index:
            if df[CSV_COLUMN_URL][i] == url:
                duplicates += 1
                return False
        path = downloadArticle(url, out_folder)
        df.loc[len(df.index)] = [url, path, 123, "test string"]
        newArticles += 1
        return True
    except Exception as err:
        errors += 1
        print("Unexpected error: ", err)


newArticles = 0
duplicates = 0
errors = 0


csvpath = os.path.join(os.getenv("TEST_DATA_FOLDER"), CSV_FILE_NAME)
if os.path.isfile(csvpath):
    df = pd.read_csv(csvpath)
else:
    df = pd.DataFrame(CSV_COLUMN_DEFINITION)

downloadFeedly(handleFeedlyItem)

# handleFeedlyItem("https://virgo.hu/szolgaltatas/e-commerce-uzletfejlesztes/")
# handleFeedlyItem("https://virgo.hu/karrier/")

df.to_csv(csvpath, index=False)

print(
    f"Added {newArticles} and skipped {duplicates} duplicates; {errors} errors occured."
)
