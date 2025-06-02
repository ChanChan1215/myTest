from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = './WebCrawler/chromedriver'  # 改成你的路徑

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.leagueofgraphs.com/champions/builds"
driver.get(url)

# 等待表格中 tr 元素出現，最多等15秒
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'table.data_table tbody tr'))
)

rows = driver.find_elements(By.CSS_SELECTOR, 'table.data_table tbody tr')

for row in rows:
    try:
        # 英雄名字通常在第一欄的 a 標籤裡
        champion_name = row.find_element(By.CSS_SELECTOR, 'td:nth-child(2) a').text
        
        # Popularity 可能在第5欄（視網頁結構調整）
        popularity = row.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text
        
        # Winrate 可能在第6欄
        winrate = row.find_element(By.CSS_SELECTOR, 'td:nth-child(6)').text
        
        print(f"英雄: {champion_name}, Popularity: {popularity}, Winrate: {winrate}")
    except Exception as e:
        print("抓取資料時錯誤:", e)
        continue

driver.quit()

