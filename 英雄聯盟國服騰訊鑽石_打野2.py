from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from pathlib import Path

def main():
    service = Service(executable_path="./WebCrawler/chromedriver")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://lolm.qq.com/act/a20220818raider/index.html"
    driver.get(url)

    # 點擊「打野」按鈕
    driver.find_element(By.CLASS_NAME, "btn-place-jungle").click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "hero-name")))

    hero_items = driver.find_elements(By.CSS_SELECTOR, "ul.data-list > li")
    print(f"共找到 {len(hero_items)} 個英雄項目")

    fileLOL = []
    for item in hero_items:
        try:
            hero_name = item.find_element(By.CLASS_NAME, "hero-name").text
            li_divs = item.find_elements(By.CLASS_NAME, "li-div")
            win_rate = li_divs[-3].text.strip()
            pick_rate = li_divs[-2].text.strip()
            ban_rate = li_divs[-1].text.strip()
            fileLOL.append([hero_name, win_rate, pick_rate, ban_rate])
        except Exception as e:
            print(f"該項目讀取失敗: {e}")

    driver.quit()

    df = pd.DataFrame(fileLOL, columns=["英雄名稱", "勝率", "登場率", "Ban率"])
    df.info()

    write_dir = Path("WebCrawler/fileLOLdiam")
    write_dir.mkdir(exist_ok=True)

    df.to_csv(write_dir / "fileLOLjungle.csv", header=True, index=False)

if __name__ == "__main__":
    main()
