import requests
from bs4 import BeautifulSoup


def main():
    url = "https://www.leagueoflegends.com/zh-tw/champions/?_gl=1*1a09ifb*_gcl_au*MTYwOTQwNjQxNi4xNzQ2NDE5OTI1*_ga*MTAyOTQ0ODg4Mi4xNzQ2NDE5OTI2*_ga_FXBJE5DEDD*MTc0NjQ1MzIxNi4zLjAuMTc0NjQ1MzIxNi4wLjAuMA.."
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    # StartUrl = "https://www.leagueoflegends.com/"
    response = requests.get(url,headers = headers)
    if response.status_code != 200:
        print(f"請求失敗,請顯示{response.status_code}")
        return
    soup = BeautifulSoup(response.text,"html.parser")

    for article in soup.select("div.sc-946e2cfc-0.dvjuUX"):
        # 查找人物對應的唯一a標籤(為何沒有按照順序出現a超連結)
        link = article.select("a")
        print(link)
        #for i in link:
            #link_url = i.get("href")  # 取得人物對應的URL         
            #title2 = i.select_one("div.sc-ce9b75fd-0.lmZfRs").text.strip() # 取得人物對應的div標籤
            #print(f"{title2}\t{link_url}")  # 依照格式輸出

        

if __name__ == "__main__":
    main()