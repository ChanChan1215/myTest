from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
from pathlib import Path

def main():
    url = "https://www.leagueofgraphs.com/champions/builds"

    service = Service(executable_path="./WebCrawler/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(15)  # 等待 JS 完整載入

    fileLOL = []

    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    for row in rows:
        try:
            # 英雄名稱從圖片 alt 取
            hero_name = row.find_element(By.CSS_SELECTOR, "td img").get_attribute("alt").strip()
        except:
            hero_name = "N/A"

        try:
            # 英雄職業實際是在 em 裡面，不是在 div.role！
            hero_position = row.find_element(By.CSS_SELECTOR, "div.name em").text.strip()
        except:
            hero_position = "N/A"

        try:
            stats = row.find_elements(By.CLASS_NAME, "progressBarTxt")
            popularity = stats[0].text.strip() if len(stats) > 0 else "N/A"
            winrate = stats[1].text.strip() if len(stats) > 1 else "N/A"
            banrate = stats[2].text.strip() if len(stats) > 2 else "N/A"
        except:
            popularity, winrate, banrate = "N/A", "N/A", "N/A"

        fileLOL.append([hero_name, hero_position, popularity, winrate, banrate])

    driver.quit()

    df = pd.DataFrame(fileLOL, columns=["英雄名稱", "英雄職業", "Popularity", "Winrate", "BanRate"])
    print(df.head(10))

    write_dir = Path("WebCrawler/LOL_USA")
    write_dir.mkdir(exist_ok=True)

    df.to_csv(write_dir / "LOL_USA_Data.csv", index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    main()
