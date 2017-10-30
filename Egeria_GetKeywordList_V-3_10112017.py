import os
from selenium import webdriver

from bs4 import BeautifulSoup
import csv
from time import sleep
from io import StringIO

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#########################################  Crome Drivers {Setup}  ##########################################
#Download Crome Web Drivers {https://chromedriver.storage.googleapis.com/index.html?path=2.33/}

#-------------------------------- INITIALIZING VARIABLE FOR DRIVERS TO WORK --------------------------------- 
#Set the PATH of Crome Driver 
chromedriver = "ENTER THE LOACTION OF YOUR CROME DRIVER"

#Variable to store Password and ID
KT_user_name = "USER_NAME"
KT_user_pass = "PASSWORD"
#-------------------------------------------------------------------------------------------------------------#

os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

#----------------------------------------- LOADING LOGIN PAGE IN THE BROWSER  --------------------------------------------#
#Loading Site {Log In page}
driver.get("https://keywordtool.io/user?destination=node")
#-------------------------------------------------------------------------------------------------------------------------#


#----------------------------------------- XPATH AND ID's TO NAVIGATE IN THE BROWSER  ------------------------------------#
#ID's of both email and password TextBox
emailFieldID = "edit-name"
passFieldID  = "edit-pass"
#ID of SearchBox
searchBoxID = "edit-keyword" 

#Xpath for Login Button 
loginButtonXpath = "//button[@value='Log in']"
#Xpath for Search Button 
searchButtonXpath = "//button[@type='submit']"
#Xpath for Downloading CSV 
downloadingButtonXpath = "(//*[contains(text(),'CSV')])[0]"
#--------------------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------LOGIN PROCESS------------------------------------------------------------#
#searching the variable
KT_search_string  = ""

#Main Working Tab of the web Browser
main_window = driver.current_window_handle

#finding Text View by ID
emailFieldElement  = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_id(emailFieldID))
passfieldElement   = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_id(passFieldID))

#finding by Xpath
loginButtonElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(loginButtonXpath))

#Clearing Saved UserID/Password
emailFieldElement.clear()
passfieldElement.clear()

#Setting UserID/Password 
emailFieldElement.send_keys(KT_user_name)
passfieldElement.send_keys(KT_user_pass)

#Clicking the Login Button
loginButtonElement.click()
#--------------------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------SEARCHING PROCESS--------------------------------------------------------#
#Search Button 
searchButtonElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(searchButtonXpath))
#Input Text in Search TextView
searchFieldElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_id(searchBoxID))

#Setting the Cursor to the list of Google Server
searchFieldElement.send_keys(Keys.TAB)
select_Drop_down = driver.switch_to.active_element
select_Drop_down.send_keys(Keys.RETURN)

#Setting The Google Server by putting it's position from the list view
position = 78
for i in range(position):
    select_Drop_down.send_keys(Keys.DOWN)
select_Drop_down.send_keys(Keys.RETURN)

#Reading CSV file
with open('test.csv','r') as csvfile: 
    reader = csv.reader(csvfile)
    for row in reader:
        #Reading line by line from the csv file 
        searchFieldElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_id(searchBoxID))
        KT_search_string = row[0]
        #Input Text in Search TextView
        searchFieldElement.send_keys(KT_search_string)
        searchButtonElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(searchButtonXpath))
        #Click on the search Button
        searchButtonElement.click()
        #Printing searched element
        print("Search success -> " + KT_search_string)

        sleep(5)
        #-----------------------------------------------FILE DOWNLOADING PROCESS--------------------------------------------------#
        #To get the CSV Downloading From Drop down menu on the Left
        actions = ActionChains(driver) 
        actions.send_keys(Keys.TAB * 13)
        actions.send_keys(Keys.RETURN)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.RETURN)
        actions.perform()   
        #-------------------------------------------------------------------------------------------------------------------------#
        
        #Sleep in order to get the load full page
        sleep(7)
        
        #Switching from Downloading pop-up window to Main Window
        driver.switch_to_window(main_window)
        
        #Loading Home location for next search from CSV file
        driver.get("https://keywordtool.io")

#-----------------------------------------------CLOSING WEB DRIVERS ---------------------------------------------------------#       
#Close Web Driver{Crome}
driver.quit()
#----------------------------------------------------------------------------------------------------------------------------#
