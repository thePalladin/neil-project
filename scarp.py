from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.support.ui as UI
from pymongo import MongoClient
client = MongoClient();
db = client.AllData;
collectionData = db.scrapped;
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

print("##state list");
print(statelist);
stDate = driver.find_element_by_id("stDate")
edDate = driver.find_element_by_id("endDate")

# sectorInput = driver.find_element_by_id("categoryId")
search = driver.find_element_by_id("searchbutton")


Sector = UI.Select(driver.find_element_by_id("categoryId"))
# sectors
print("##Sector");
print(Sector);


sectors = []
for option in Sector.options:
        sectors.append(option.text)
sectors = sectors[1:]

print("##sector");
print(sectors);

stateId = UI.Select(driver.find_element_by_id("stateId"))
year = 2012
time.sleep(3)
while year<2019:

    stDate.clear()
    edDate.clear();

    startDate = "01/01/"+str(year);
    endDate = "31/12/"+str(year);

    stDate.send_keys(startDate);
    edDate.send_keys(endDate);

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
                    
                    case = driver.find_element_by_css_selector("#placeholder1 > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > a:nth-child(1)");
                    complainant = driver.find_element_by_css_selector("#placeholder1 > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)");
                    respondent = driver.find_element_by_css_selector("#placeholder1 > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)");
                    complainantAdv = driver.find_element_by_css_selector("#placeholder1 > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(4)");
                    respondentAdv = driver.find_element_by_css_selector("#placeholder1 > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(5)");
                    dateOfDisposal = driver.find_element_by_css_selector("#placeholder1 > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(6)");
                    dateOfUpload = driver.find_element_by_css_selector("#placeholder1 > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(7)");
                    getPDF = driver.find_element_by_css_selector("#placeholder1 > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(8) > a:nth-child(1)").get_attribute("href");

                    if table.text[0] == 'S':

                        finalData = {
                        'startDate' : startDate,
                        'endDate' : endDate,
                        'State' : state,
                        'District' : district,
                        'Sector' : sect,
                        'CaseNo' : case.text,
                        'Complainant' : complainant.text,
                        'Respondent' : respondent.text,
                        'ComplainantAdv' : complainantAdv.text,
                        'RespondentAdv' : respondentAdv.text,
                        'dateOfDisposal' : dateOfDisposal.text,
                        'dateOfUpload' : dateOfUpload.text,
                        'PDF' : getPDF
                        }
                        print(finalData);
                        collectionData.insert_one(finalData);
                    else:
                        print(sect+'NO')
                except NoSuchElementException:
                        print(sect+"Does not Exist")
# data
driver.quit()
