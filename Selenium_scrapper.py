#this program will use selenium instead of beautiful soup to scrape the data from a site
#This is to ensure that the scrapper program can interact with a dynamic site
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service
import pandas
import pandas as pd
#the path file of your driver
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
pages_URL=[]
while not_last_pg:
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
                #we then get the tag for the link of the next page
                try:
                    each_link=header.find_element(By.TAG_NAME, "a")
                    url=(each_link.get_attribute("href"))
                    pages_URL.append(url)
                except Exception as e:
                    print(f"A link wasn't found for {title_txt}" )
            except Exception as e:
                print(f"The Designated Element wasn't found in page {pages}" )
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
#quit driver and send all the titles and URL to an Excel file
driver.quit()
# Create a DataFrame to store scraped data
df = pd.DataFrame({
    'Page Titles': page_titles,
    'URL': pages_URL
})
# Define the output file path for Excel
output_file = r'C:\Users\TUBORR\Desktop\WEB3 DEV JOURNEY\PYTHON\Exercises\Web-Scraper\Google_titles_Url_Scraped.xlsx'
# Write DataFrame to Excel
try:
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Search_results', index=False)
    print(f"Data set has been scraped successfully into '{output_file}'. Thank you.")
except Exception as e:
    print(f"An error occurred when trying to store data: {e}")
