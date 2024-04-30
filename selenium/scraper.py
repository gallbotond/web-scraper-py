import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

website = 'https://www.emag.ro/search/gaming+laptop'
executable_path = 'drivers/chromedriver-win64/chromedriver.exe'

service = Service(executable_path)
driver = webdriver.Chrome(service=service)
driver.get(website)


# Wait for the dropdown to be clickable
dropdown_btn = driver(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "sort-control-btn-dropdown"))
)

# Click on the dropdown button to open the options
dropdown_btn.click()

# Wait for the dropdown menu to be visible
dropdown_menu = driver(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "listing-sorting-dropdown"))
)

# Find the "100 pe pagina" option and click it
option_100_per_page = dropdown_menu.find_element_by_xpath("//a[contains(text(), '100 pe pagina')]")
option_100_per_page.click()


time.sleep(10)
driver.quit() 