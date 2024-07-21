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
search = driver.find_element(By.NAME, "q")
#the above is the search box input field
search.send_keys("test")
search.send_keys(Keys.RETURN)
pages=1
not_last_pg=True
page_titles=[]

while not_last_pg==True:
    try:
        result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "rso"))
        )
        headers = result.find_elements(By.CLASS_NAME, "MjjYud")
        for header in headers:
            #to prevent crashing we use the try and except to catch erros and ensure our code continues to search for the designated elements
            try:
                each_title=header.find_element(By.CSS_SELECTOR, "h3.LC20lb")
                title_txt=each_title.text
                page_titles.append(title_txt)
            except Exception as e:
                print("The Designated Element wasn't found" )
        #now we need to find the next page
        nxt_pg_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "pnnext"))
        )
        #upon finding it now click on the button
        nxt_pg_button.click()
        pages+=1
        #if we cannot find this link we need to break
    except Exception as e:
        print(f"The next Button is not present after {pages} pages")
        not_last_pg=False
#quit driver and display all the titles
print(page_titles)
driver.quit()
#we can also find elements by the text that will give a link upon clicking
#this is done with the find_element(By.LINK_TEXT)
#then link.click
