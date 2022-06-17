import json
import time
import httpx
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

tag = input("Input the main tag: ")
SORT_MEMBERS = input("Search in 'SORT BY MEMBERS' mode? [Y/n]: ")
PAGES = 50

ALL_TAGS = {}


BASE_URL = "https://disboard.org/servers/tag/"

def get_data(tag, page):
    end = ""
    url = BASE_URL + tag + "/" + str(page)
    if (SORT_MEMBERS.lower() == 'y'):
        end = "?sort=-member_count"
    
    url = url + end
    res = httpx.get(url)
    parsed = BeautifulSoup(res.content, features="lxml")
    tagsDivs = parsed.find_all("div", {"class": "server-tags"})
    for div in tagsDivs:
        tags = div.find_all("li")
        for tag in tags:
            text = tag.find("a").text.replace("\n", "").replace(" ", "")
            if text not in ALL_TAGS:
                ALL_TAGS[text] = 1
            else:
                ALL_TAGS[text] += 1
    return ALL_TAGS

if __name__ == "__main__":
    print("Starting...")
    for i in range(1, PAGES+1):
        print("Page: " + str(i))
        data = get_data(tag, i)
        tags = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
        for key, value in tags.items():
            if (value > 100):
                print(key + ": " + str(value))
        print("")
        time.sleep(5)
    
    with open("tags.json", "w") as f:
        json.dump(tags, f, indent=4)
    
