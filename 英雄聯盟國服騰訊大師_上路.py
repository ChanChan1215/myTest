from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from pathlib import Path





def main():
    service = Service(executable_path="./WebCrawler/chromedriver")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://lolm.qq.com/act/a20220818raider/index.html"
    #https://lolm.qq.com/act/a20220818raider/index.html
    driver.get(url)
    #點選"打野"的按鈕
    masterClk = driver.find_element(By.CSS_SELECTOR,"a.btn-dan[data-dan='2']")
    masterClk.click()
    driver.find_element(By.CLASS_NAME, "btn-place-top").click()
    #print(f"driver.current_url:\n{driver.current_url}")
    # 等待網頁元素載入
    time.sleep(10)

    # 找到所有英雄的li項目
    hero_items = driver.find_elements(By.CSS_SELECTOR, "ul.data-list > li")
    fileLOL = []
    for item in hero_items:
        # 抓英雄名字
        hero_name = item.find_element(By.CLASS_NAME, "hero-name").text
        
        # 抓勝率 - 請依實際class調整
        # 這裡假設勝率在class="li-div" 且位置固定，比如第4個 li-div
        li_divs = item.find_elements(By.CLASS_NAME, "li-div")
        win_rate = li_divs[-3].text.strip()  # 這邊示範抓最後一個li-div，請依網站調整
        
        # 登場率你可以看li_divs中的其他位置，這是示意
        # 例如，假設登場率是倒數第二個 li-div
        pick_rate = li_divs[-2].text.strip()
        #Banrate
        ban_rate = li_divs[-1].text.strip()
        fileLOL.append([hero_name, win_rate, pick_rate,ban_rate])
        #print(fifleLOL_path)

    driver.quit()
    df = pd.DataFrame(fileLOL, columns=["英雄名稱", "勝率", "登場率","Ban率"])
    df.info()
    #---------------------------------
    write_dir = Path("WebCrawler/LOL_MS")
    write_dir.mkdir(exist_ok=True)

    df.to_csv(
        write_dir/"LOL_MS_Top.csv",
        header=True,
        index=False
    )

#寫入CSV
#with open("lol_hero_stats.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
        #writer = csv.writer(csvfile)

        # 寫入表頭
        #writer.writerow(["英雄名稱", "勝率", "登場率"])

        # 寫入所有資料
        #writer.writerows(fifleLOL_path)

    #print("✅ 資料已成功寫入 lol_hero_stats.csv")


if __name__ == "__main__":
    main()