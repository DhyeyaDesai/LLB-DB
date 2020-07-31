#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException


# In[ ]:


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


# In[ ]:


driver = webdriver.Firefox(executable_path="C:\\Python38\\geckodriver.exe")
driver.get("https://www.ilsos.gov/corporatellc/CorporateLlcController")


# In[ ]:


alphabets = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
nums= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
#"200" is not done 

searchKeys = []
temp = ""

for a in nums:
    for b in alphabets:
        for c in alphabets:
            temp = a + b + c
            if temp>="408":
                searchKeys.append(temp)


# In[ ]:


alphabets = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
nums= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
#"200" is not done 

searchKeys = []
temp = ""

for a in nums:
    for b in alphabets:
        for c in alphabets:
            for d in alphabets:
                temp = a + b + c +d
                if temp>="360b":
                    searchKeys.append(temp)


# In[ ]:


data = {'FileNumber': [],
    'BusinessName': [],
    'Address': [],
    'Date': [],
    'AgentName': [],
    'AgentAddress': []
    }

df = pd.DataFrame(data)


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


df.to_csv("dfNUM.csv")

