import requests
from bs4 import BeautifulSoup
#動態
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
from pathlib import Path

def main():
    url = "https://www.leagueofgraphs.com/champions/builds"
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    response = requests.get(url,headers = headers)
    if response.status_code != 200:
        print(f"請求失敗,請顯示{response.status_code}")
        return
    soup = BeautifulSoup(response.text,"html.parser")
    #英雄名字
    #for hero_item in soup.select("span.name"):
        #hero_name = hero_item.text.strip()
        #print(hero_name)
    #英雄位置
    fileLOL = []
    for hero_item2 in soup.select("i"):
        hero_position = hero_item2.text.strip()
        fileLOL.append([hero_position])
    df = pd.DataFrame(fileLOL, columns=["英雄職業"])
    df.info()   
    write_dir = Path("WebCrawler/LOL_USA")
    write_dir.mkdir(exist_ok=True)

    df.to_csv(
        write_dir/"LOL_USA_Position.csv",
        header=True,
        index=False
    )
    #---------------------------------------------
    #動態抓取
    #service = Service(executable_path="./WebCrawler/chromedriver")
    #options = webdriver.ChromeOptions()
    #driver = webdriver.Chrome(service=service, options=options)

    #url = "https://www.leagueofgraphs.com/champions/builds"
    #driver.get(url)
    #time.sleep(15)  # 等待 JS 載入

    
    #hero_data = driver.find_elements(By.CLASS_NAME, "progressBarTxt")
    #for item in hero_data:
        #hero_data_content = item.text.strip()
        #print(hero_data_content)
    
    #fileLOL.append([hero_name,hero_position,hero_data_content])
    #driver.quit()
    #df = pd.DataFrame(fileLOL, columns=["英雄名稱", "英雄職業", "英雄各項數據"],)
    #df.info()

    #write_dir = Path("WebCrawler/LOL_USA")
    #write_dir.mkdir(exist_ok=True)

    #df.to_csv(
        #write_dir/"LOL_USA_Data.csv",
        #header=True,
        #index=False
    #)
    #for allItem in hero_items:
        #英雄名稱
        #try:
            #hero_name = allItem.find_elements(By.CLASS_NAME, "name") 
        #except:
            #hero_name = "NA"
            #print(hero_name )
        #英雄職業
        #try:
            #hero_position = allItem.find_element(By.CSS_SELECTOR, "i")
        #except:
            #hero_position = "NA"
            #print(hero_position)
        #英雄各項數據
        #try:
            #hero_data = allItem.find_elements(By.CLASS_NAME, "progressBarTxt")
        #except:
            #hero_data = "NA"
            #print(hero_data)
        
        
    
        #print(hero_data_content)
    #for row in rows:
        #hero_data = row.find_element(By.CSS_SELECTOR, "td div.name").text
    #for hero_item3 in soup.select("div.progress"):
        #hero_data = hero_item3.text.strip()
        #print(hero_data)
    
    
        











if __name__ == "__main__":
    print("===================================")
    main()
    print("===================================")