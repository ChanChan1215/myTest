import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path 

def main():
    url="https://www.leagueoflegends.com/zh-tw/champions/?_gl=1*1stfjmi*_gcl_aw*R0NMLjE3NDczMTM1MTIuQ2owS0NRandvWmJCQmhEQ0FSSXNBT3FNRVpWUXQyb3BqbW1aTHYtUkV3Z0NzcEpWX1BIWnpuWHlZZ0Fmd0FzRlhIWXhMSjBCRC1TdVd4NGFBcWlHRUFMd193Y0I.*_gcl_au*MTYwOTQwNjQxNi4xNzQ2NDE5OTI1*_ga*MTAyOTQ0ODg4Mi4xNzQ2NDE5OTI2*_ga_FXBJE5DEDD*czE3NDc0MDM2MjkkbzEwJGcwJHQxNzQ3NDAzNjI5JGowJGwwJGgw"
    headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers = headers)
    if response.status_code != 200: 
        print(f"請求失敗，status code: {response.status_code}")
        return
    saveImage = Path("WebCrawler/saveLOLImages")
    saveImage.mkdir(exist_ok = True)
    soup = BeautifulSoup(response.text, "html.parser")
    for imageUrl in soup.find_all(attrs={"aria-label":True}):
        imageName = imageUrl.text.strip()
        break   
        #print(imageName)
    imageItem = soup.find(attrs={"aria-label":"亞菲利歐"})
        #print(imageItem)
    firstImg = imageItem.find("img")
    image = firstImg.get("src")
    imgSrc = requests.get(image)
        
    #for imageItem in soup.find_all("img"):
        #imageSrc = imageItem.get("src")
        #image = requests.get(imageSrc)
        #print(imageSrc)
        #imageSrc2 = requests(imageSrc)
    imageContent = imgSrc.content
    path = saveImage/f"{imageName}.jpg"
    with open(path, "wb") as file:
            file.write(imageContent)
    print(f"{path} 存檔完成")
    #GET https://u.gg/api/v1/champions/Aphelios/overview?region=world&rank=diamond_plus&tier=all










if __name__ == "__main__":
    print("===================================")
    main()
    print("===================================")