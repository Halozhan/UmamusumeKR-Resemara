from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
# import chromedriver_autoinstaller 구버전
# import os
import time

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
try:
    from ASUS_ROUTER_CONFIG import *
except:
    print("라우터 구성에 필요한 계정 정보가 없습니다.")

def importChromeDriver() -> webdriver.Chrome:
    # 구버전
    # if not os.path.isdir("ChromeDriver"): # 크롬 드라이버 폴더 생성
    #     os.makedirs("ChromeDriver")

    # chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    # driver_path = f"./ChromeDriver/{chrome_ver}/chromedriver.exe"
    # if os.path.exists(driver_path):
    #     # print("ChromeDriver is installed: " + driver_path)
    #     pass
    # else:
    #     print("install the ChromeDriver. VER: " + chrome_ver)
    #     chromedriver_autoinstaller.install(path="./ChromeDriver")
    
    options = webdriver.ChromeOptions()
    options.add_argument("incognito")
    options.add_argument("headless")
    options.add_argument("no-sandbox")
    options.add_argument("disable-setuid-sandbox")
    options.add_argument("disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    # driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def ASUS_Change_MAC(isReboot=False):
    driver = importChromeDriver()

    try:
        try:
            driver.get("http://router.asus.com/")
        except:
            driver.get(GATEWAY_ADDRESS)
        driver.implicitly_wait(5)
        
        id = driver.find_element(by=By.NAME, value="login_username")
        id.send_keys(ID)

        pw = driver.find_element(by=By.NAME, value="login_passwd")
        pw.send_keys(PW)

        driver.find_element(by=By.CLASS_NAME, value="button").click()

        if isReboot:
            driver.find_element(by=By.XPATH, value='//*[@id="TopBanner"]/div/a[2]/div/span').click()
            driver.implicitly_wait(0.5)

            driver.switch_to.alert
            driver.implicitly_wait(0.5)

            Alert(driver).accept()

            print("Router is rebooting")
            time.sleep(210)

            driver.quit()
        else:
            try:
                driver.get("http://router.asus.com/Advanced_WAN_Content.asp")
            except:
                driver.get(GATEWAY_ADDRESS+"Advanced_WAN_Content.asp")
            driver.implicitly_wait(5)
            
            MACAdd = driver.find_element(by=By.NAME, value="wan_hwaddr_x")
            MAC_Address = MACAdd.get_attribute("value")

            MAC_Address = MAC_Address.replace(":", "")
            asdf = MAC_Address
            asdf = int("0x"+asdf, 16)
            asdf = asdf + 1
            # print(asdf)
            asdf = hex(asdf)
            asdf = asdf.replace("0x", "")
            index = 0
            address = ""
            for i in asdf:
                if index % 2 == 1:
                    address += i
                    address += ":"
                    index += 1
                    continue
                address += i
                index += 1
            MAC_Address = address[:-1]
                
            print("New MAC Address:", MAC_Address)
            MACAdd.clear()
            MACAdd.send_keys(MAC_Address)
        
            driver.find_elements(by=By.XPATH, value='//*[@id="FormTitle"]/tbody/tr/td/div[7]/input')[0].click()
            # driver.find_elements(by=By.CLASS_NAME, value="button_gen")[1].click()
            time.sleep(60)

            driver.quit()
    except:
        pass
        
    
if __name__ == "__main__":
    ASUS_Change_MAC(True)