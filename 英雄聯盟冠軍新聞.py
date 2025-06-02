import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def main():
    url = "https://www.epochtimes.com/b5/12/10/14/n3705582.htm"
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers = headers)
    if response.status_code != 200: 
        print(f"請求失敗，status code: {response.status_code}")
        return
    soup = BeautifulSoup(response.text, "html.parser")
    #抓標題
    #select抓出來一定是list.所以一定要再取出來一次
    item = soup.select("div>h1.title")
    titleItem = item[0]
    titleWord = titleItem.text.strip()

    #抓內容(問題:有沒有辦法組合再一起)
    item2 = soup.select("div>p")
    contentItem = item2[0]
    content = contentItem.text.strip()

    item3 = soup.select("div>p")
    contentItem2 = item3[1]
    content2 = contentItem2.text.strip()

    LOLChampion = f"{titleWord}\n{content}{content2}"
    print(LOLChampion)
    
    











if __name__ == "__main__":
    print("===================================")
    main()
    print("===================================")

