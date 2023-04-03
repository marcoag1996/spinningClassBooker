from selenium import webdriver
""""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC"""

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import Select

# Create options to avoid closing browser
options = Options()
options.add_experimental_option("detach", True)

# Create instance of chrome 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

URL = "https://xcycle.mx/index.html"

# Open browser
driver.get(URL)

# find all the links / ancher tags
links = driver.find_elements("xpath", "//a[@href]")

# Iterate through links and select "reserva"
for link in links:
    if "Reserva" in link.get_attribute('innerHTML'):
        link.click()
        break

# Get form of sucursales
sucursales = driver.find_elements("xpath", "//select[contains(@id, 'selectSuc')]")

# Select the one that has Milenio in the name
for sucursal in sucursales:
    if "Milenio" in sucursal.get_attribute('innerHTML'):
        select = Select(sucursal)
        # sucursal.click() just opens the selection box
    # print(sucursal.get_attribute('innerHTML'))

# Select value from the form
select.select_by_value("Milenio")

# Open calendar
semana_calendar = driver.find_element("xpath", "//input[contains(@class, 'select-class')]")
semana_calendar.click()

# Select a day, deprecated easier way to use xpath to get specific day like the one of current_day var
# days = driver.find_elements("xpath", "//td[contains(@class, 'day')]")

#rows = driver.find_elements("xpath", "//table[contains(@class, 'table-condensed')][./tr]")
rows = driver.find_elements("xpath", "//div[contains(@class, 'datetimepicker-days')]//tbody//tr")

# print rows
print("PRINT ROWS")
for r in rows:
    print(r.get_attribute('innerHTML'))

# Modify the current date 
# TODO: Find the way to get the date automatically
date = "29"
current_day = driver.find_element("xpath", "//table//td[contains(text(), '%s')]" %date)

# Get parent tr from the td (cell picked "day")
week = current_day.find_element("xpath", "./..")
print("PRINT WEEK")
print(week.get_attribute('innerHTML'))
# Get index of the row corresponding to the week in the calendar
week_index = rows.index(week)
print(week_index)

# get day(cell) of next week
# tr[] and td[] is not zero-index in counts 1,2,3..
next_week_day = driver.find_element("xpath", "//div[contains(@class, 'datetimepicker-days')]//tbody//tr[%s+2]//td[1]" %week_index)

# click the day of the calendar
# make the cell actionable / clickable
actions = ActionChains(driver)
col_index = current_day.get_attribute("cellIndex")
#print(col_index)
actions.move_to_element(next_week_day)
actions.click()
actions.perform()



# TODO: Select instructor based on the hour
# login to my account to finish reservation
# repeat process for the three week days (Monday, Wednesday, Saturday(maybe))
"""
options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(
    options=options,
)

driver.get(URL)

time.sleep(4000)

button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html//div[@class='container']//a[@href='/index.html']"))

)

button.click()

"""