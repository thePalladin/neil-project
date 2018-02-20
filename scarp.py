from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.support.ui as UI
import time
import json
import sys
import signal

driver=webdriver.Chrome()
driver.get("http://cms.nic.in/ncdrcusersWeb/search.do?method=loadSearchPub")

dof = driver.find_element_by_id("dtof")
dof.click()

searchBy = driver.find_element_by_id("searchBy")
searchBy.send_keys("Sector")
time.sleep(0.2)
time.sleep(0.2)



with open('selectors.json') as json_file:
    area = json.load(json_file)

statelist = []

for i in area.keys():
    statelist.append(i)
stDate = driver.find_element_by_id("stDate")
endDate = driver.find_element_by_id("endDate")

# sectorInput = driver.find_element_by_id("categoryId")
search = driver.find_element_by_id("searchbutton")


Sector = UI.Select(driver.find_element_by_id("categoryId"))
# sectors


sectors = []
for option in Sector.options:
        sectors.append(option.text)
sectors = sectors[1:]


stateId = UI.Select(driver.find_element_by_id("stateId"))
year = 2012
time.sleep(3)
while year<2019:

    stDate.clear()
    stDate.send_keys("01/01/"+str(year))
    endDate.clear()
    endDate.send_keys("31/12/"+str(year))
    year = year + 1
    for state in statelist:
        print(state)
#             stateId.clear()

        stateId.select_by_visible_text(state)
        time.sleep(0.5)
        for district in area[state]:
            districtId = UI.Select(driver.find_element_by_id("districtId"))
#                 districtId.clear()
            print(district)
            districtId.select_by_visible_text(district)
            time.sleep(0.5)
            for sect in sectors:
                Sector.select_by_visible_text(sect)
                time.sleep(2)
                search.click()
                time.sleep(2)
                try:
                    table = driver.find_element_by_id("para1")
                    if table.text[0] == 'S':
                        print(sect +"Exists")
                    else:
                        print(sect+'NO')
                except NoSuchElementException:
                        print(sect+"Does not Exist")
# data
driver.quit()
