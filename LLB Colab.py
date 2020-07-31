#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install selenium')
get_ipython().system('apt-get update # to update ubuntu to correctly run apt install')
get_ipython().system('apt install chromium-chromedriver')
get_ipython().system('cp /usr/lib/chromium-browser/chromedriver /usr/bin')
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)


# In[ ]:


import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from google.colab import drive

drive.mount('/content/drive')

df = pd.read_csv("/content/drive/My Drive/LLB/dfALP.csv", index_col="Unnamed: 0")
# df

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get("https://www.ilsos.gov/corporatellc/CorporateLlcController")
a = driver.find_elements_by_name("type")
a[2].click()
submitBtn = driver.find_element_by_id("subCon")
submitBtn.click()


# In[ ]:


alphabets = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
#"200" is not done 

searchKeys = []
temp = ""

for a in alphabet:
    for b in alphabets:
        for c in alphabets:
            temp = a + b + c
            if temp>="all":
                searchKeys.append(temp)


# In[ ]:


for searchKey in searchKeys:
    try:
        searchBar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@class='form-control' and @maxlength='30']"))
        )
        searchBar.send_keys(searchKey)
        submitBtn = driver.find_element_by_xpath("//*[@name='next'][@type='submit']")
        submitBtn.click()

    except Exception as e:
        print(e)

    while True:
        list1 = []
        
        if check_exists_by_xpath("//*[@class = 'black10b']"):
            break
#         time.sleep(0.5)

        try:
            searchBar = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@class = 'table table-striped table-hover']"))
            )
            
            mytable = driver.find_element_by_xpath("//*[@class = 'table table-striped table-hover']")

        except Exception as e:
            print(e)
        for row in mytable.find_elements_by_css_selector("tr"):
            for data in row.find_elements_by_css_selector("td"):
                links = data.find_elements_by_css_selector("a")
                if links!=[]:
                    list1.append(links[0].text)

        for l in list1:
            print(l)
            try:
                link = driver.find_element_by_xpath("//*[contains(text(), \""+l+"\")]")
                link.click()
                record = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@class=\"col-sm-8 col-md-10\"]"))
                )
                basicinfo = driver.find_elements_by_xpath("//*[@class = \"col-sm-8 col-md-10\"]")
                FileNumber = basicinfo[3].text
                BusinessName = basicinfo[4].text
                einfo = driver.find_elements_by_xpath("//*[@class = \"col-sm-9\"]")
                address = str(einfo[12].text).replace("\n", ", ")
                date = einfo[15].text
                agent_name = einfo[18].text
                agent_address = str(einfo[19].text).replace("\n", ", ")
                row = {'FileNumber': FileNumber, 'BusinessName': BusinessName, 'Address': address, 'Date': date, 'AgentName': agent_name, 'AgentAddress': agent_address}
                df = df.append(row, ignore_index=True)
                driver.back()

            except Exception as e:
                print(e)
#         time.sleep(0.5)

        if check_exists_by_xpath("//*[@class = \"btn btn-default\" and @value='More' and @name='command']"):
            more = driver.find_element_by_xpath("//*[@class = \"btn btn-default\" and @value='More' and @name='command']")
            more.click()
        else:
            break
            
    driver.get("https://www.ilsos.gov/corporatellc/CorporateLlcController")
    a = driver.find_elements_by_name("type")
    a[2].click()
    submitBtn = driver.find_element_by_id("subCon")
    submitBtn.click()
    lastkey = searchKey


# In[ ]:


df.to_csv("/content/drive/My Drive/LLB/dfALP.csv")

