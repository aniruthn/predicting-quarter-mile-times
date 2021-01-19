from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import csv

array_links = []
array_all_links = []
otherpages = []
cars_links = []

options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
driver.set_window_size(1280, 1024)

driver.get('http://www.dragtimes.com/browse.php')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
big_div = soup.select('div.list-area.single-list')
unordered_list = big_div[0].find('ul')
links = unordered_list.find_all('a')
for tag in links:
    array_links.append(tag['href'])
array_links = array_links[1:]

for link in array_links:
    url = 'http://www.dragtimes.com/' + link
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    td = soup.find('td')
    all_records = td.find('a')
    array_all_links.append(all_records['href'])

for link in array_all_links:
    url = 'http://www.dragtimes.com/' + link
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = soup.find('div', class_='details')
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        if row.find('a'):
            cars_links.append(row.find('a')['href'])
    #account for pagination
    pages = soup.find_all('center')
    pages = pages[len(pages) - 1]
    pages = pages.find_all('a')
    if pages and '?resultpage' in pages[0]['href']:
        otherpages = []
        for page in pages:
            otherpages.append(link + page['href'])
        otherpages = otherpages[:len(otherpages)-1]
        for link in otherpages:
            url = 'http://www.dragtimes.com/' + link
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            soup = soup.find('div', class_='details')
            table = soup.find('table')
            rows = table.find_all('tr')
            for row in rows:
                if row.find('a'):
                    cars_links.append(row.find('a')['href'])

with open('cardatafinal.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['1/4 Mile ET', '1/4 Mile MPH', '1/8 Mile ET', '1/8 Mile MPH', '0-60 Foot ET', 'HP', 'Torque', 'Make', 'Model', 'Type', 'Year', 'Weight'])
    for link in cars_links:
        url = 'http://www.dragtimes.com/' + link
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tables = soup.find_all('div', class_='table')
        tables = [table.find('ul') for table in tables]
        if tables and isinstance(tables, list) and len(tables) >= 3:
            performance_data = [li.find('span').text for li in tables[0].find_all('li', limit=5)] #1/4 Mile ET, 1/4 Mile MPH, 1/8 Mile ET, 1/8 Mile MPH, 0-60 Foot ET
            dyno_data = [li.find('span').text for li in tables[1].find_all('li', limit=2)] #HP, Torque
            car_data = [li.find('span').text for li in tables[2].find_all('li', limit=9)]
            car_data = car_data[0:4] + [car_data[8]] #Make, Model, Type, Year, Weight
            data_to_be_written = performance_data + dyno_data + car_data
            if data_to_be_written[5] and (data_to_be_written[5] != 'Click HERE to estimate') and data_to_be_written[11] and (data_to_be_written[11] != '0'):
                writer.writerow(data_to_be_written)

driver.close()
driver.quit()