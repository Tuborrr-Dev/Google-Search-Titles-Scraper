#this program will use selenium instead of beautiful soup to scrape the data from a site
#This is to ensure that the scrapper program can interact with a dynamic site
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service

PATH = "C:\\Program Files (x86)\\chromedriver.exe"

# Create a Service object
service = Service(PATH)
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")
#this is used to close the tab but if you want to display once youll say.quit
#you can use the driver command to also get information about the page such as the page title
print(driver.title)
#we can search for elements in out html using different methods
#either by ID, Name or Class in descending order can we identify elements
search = driver.find_element(By.NAME, "q")
#the above is the search box input field
search.send_keys("test")
search.send_keys(Keys.RETURN)
#the above sends keys into the variable
#using waits we can wait for the presence of an element before we start printing a value
try:
    result = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "res"))
    )
    headers = result.find_element(By.CLASS_NAME, "g Ww4FFb vt6azd tF2Cxc asEBEc")
    for header in headers:
        each_page_title = header.find_element(By.CLASS_NAME, "LC20lb MBeuO DKV0Md")
        print(each_page_title.text)
finally:
    driver.quit()
