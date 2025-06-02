from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def main():
    service = Service(executable_path="./WebCrawler/chromedriver")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://lolm.qq.com/act/a20220818raider/index.html"
    driver.get(url)

    time.sleep(3)  # 等待初始頁面載入

    # 職業分類的中文標籤（依網站順序）
    roles = ["上單", "打野"]
    role_index = [0, 1]  # 上單是第0個、打野是第1個

    for i, role in zip(role_index, roles):
        # ✅ 正確的分類 tab selector
        position_tabs = driver.find_elements(By.CSS_SELECTOR, "div.position-list > div")
        print(f"抓到 {len(position_tabs)} 個職業分類 tab")

        if i >= len(position_tabs):
            print(f"⚠️ 無法點選第 {i} 個職業分類（{role}），請檢查 selector 或網站結構")
            continue

        position_tabs[i].click()
        time.sleep(3)  # 等待資料更新

        hero_items = driver.find_elements(By.CSS_SELECTOR, "ul.data-list > li")
        print(f"\n【{role}】")

        for item in hero_items:
            try:
                hero_name = item.find_element(By.CLASS_NAME, "hero-name").text
                li_divs = item.find_elements(By.CLASS_NAME, "li-div")

                if len(li_divs) >= 3:
                    win_rate = li_divs[-3].text.strip()
                    pick_rate = li_divs[-2].text.strip()
                else:
                    win_rate = pick_rate = "N/A"

                print(f"英雄名稱: {hero_name}，勝率: {win_rate}，登場率: {pick_rate}")
            except Exception as e:
                print(f"錯誤: {e}")
                continue

    driver.quit()

if __name__ == "__main__":
    main()
