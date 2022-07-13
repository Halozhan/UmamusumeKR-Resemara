from selenium import webdriver
import chromedriver_autoinstaller
import os
import time
try:
    from ASUS_ROUTER_CONFIG import *
except:
    print("라우터 구성에 필요한 계정 정보가 없습니다.")

def Change_Mac_Address():
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f"./ChromeDriver/{chrome_ver}/chromedriver.exe"
    if os.path.exists(driver_path):
        print("ChromeDriver is installed: " + driver_path)
    else:
        print("install the ChromeDriver. VER: " + chrome_ver)
        chromedriver_autoinstaller.install(path="./ChromeDriver")
    
    driver = webdriver.Chrome(driver_path)

    try:
        driver.get(GATEWAY_ADDRESS)
        driver.implicitly_wait(5)
        
        id = driver.find_element_by_name("login_username")
        id.send_keys(ID)

        pw = driver.find_element_by_name("login_passwd")
        pw.send_keys(PW)

        driver.find_element_by_class_name("button").click()

        
        driver.get(GATEWAY_ADDRESS+"Advanced_WAN_Content.asp")
        driver.implicitly_wait(5)
        
        MACAdd = driver.find_element_by_name("wan_hwaddr_x")
        MAC_Address = MACAdd.get_attribute("value")

        MAC_Address = MAC_Address.replace(":", "")
        asdf = MAC_Address
        asdf = int("0x"+asdf, 16)
        asdf = asdf + 1
        print(asdf)
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
            
        print(MAC_Address)
        MACAdd.clear()
        MACAdd.send_keys(MAC_Address)

        driver.find_elements_by_xpath('//*[@id="FormTitle"]/tbody/tr/td/div[7]/input')[0].click()
        
        time.sleep(7)
    except:
        pass
    
if __name__ == "__main__":
    Change_Mac_Address()