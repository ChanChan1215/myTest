import requests
from bs4 import BeautifulSoup


def main():
    url = "https://www.leagueoflegends.com/zh-tw/champions/?_gl=1*1a09ifb*_gcl_au*MTYwOTQwNjQxNi4xNzQ2NDE5OTI1*_ga*MTAyOTQ0ODg4Mi4xNzQ2NDE5OTI2*_ga_FXBJE5DEDD*MTc0NjQ1MzIxNi4zLjAuMTc0NjQ1MzIxNi4wLjAuMA.."
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url,headers = headers)
    if response.status_code != 200:
        print(f"請求失敗,請顯示{response.status_code}")
        return
    soup = BeautifulSoup(response.text,"html.parser")
    allTitle = "https://www.leagueoflegends.com"
    for article in soup.select("div.sc-946e2cfc-0.dvjuUX"):
        title = article.select("a")
        for item in title:
            getUrl = item.get("href")
            title2 = item.select_one("div.sc-ce9b75fd-0.lmZfRs").text.strip()
            print(f"{allTitle}{getUrl}\n{title2}")
        #title = article.select_one(".sc-ce9b75fd-0").text.strip()
    #尚未抓到超連結
        #a = article.select_one(".sc-985df63-0 > a[href]")
        #link = a["href"] if a else None
    #chatgpt建議 
        #print(link)





if __name__ == "__main__":
    print("===================================")
    main()
    print("===================================")