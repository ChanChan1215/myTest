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
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(15)  # JS 載入等待

    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    positions = []

    for row in rows:
        try:
            hero_position = row.find_element(By.CSS_SELECTOR, "div.txt > em").text.strip()
        except:
            hero_position = "N/A"

        positions.append([hero_position])

    driver.quit()

    df = pd.DataFrame(positions, columns=["英雄職業"])
    print(df.head(10))

    write_dir = Path("WebCrawler/LOL_USA")
    write_dir.mkdir(exist_ok=True)

    df.to_csv(write_dir / "LOL_USA_Position.csv", index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    print("====== Start ======")
    main()
    print("======= End =======")
