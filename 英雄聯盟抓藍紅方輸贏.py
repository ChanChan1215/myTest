import requests
from bs4 import BeautifulSoup

def main():
    url = "https://www.leagueofgraphs.com/stats/blue-vs-red"
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }


    response = requests.get(url,headers = headers)
    if response.status_code != 200:
        print(f"請求失敗,請顯示{response.status_code}")
        return
    soup = BeautifulSoup(response.text,"html.parser")
    #blue_win
    items = soup.select("span.biggest_number.wgbluefont")
    rankSolo_blue = items[0].text.strip()
    rankAram_blue = items[1].text.strip()
    print(f"rankSolo_blue {rankSolo_blue}")
    print(f"rankAram_blue {rankAram_blue}")
    #blue_loss
    items_blue_loss = soup.select("span.smallest_number.wgbluefont")
    rankRankedFlex_blue = items_blue_loss[0].text.strip()
    print(f"rankRankedFlex_blue {rankRankedFlex_blue}") 

    #red_win
    items_red_win_item1 = soup.select("span.biggest_number.wgredfont")
    items_red_win_RankedFlex = items_red_win_item1[0].text.strip()
    print(f"items_red_win_RankedFlex {items_red_win_RankedFlex}")

    
        








if __name__ == "__main__":
    print("===================================")
    main()
    print("===================================")