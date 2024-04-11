# Importing necessary libraries
import pandas as pd                                                 
from selenium import webdriver                              
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait             
from selenium.webdriver.support import expected_conditions as EC    
from bs4 import BeautifulSoup
import time

# Setting up Selenium webdriver
url = "https://www.whoscored.com/Regions/250/Tournaments/12/Europe-Champions-League"

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get(url)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'seasons'))
)

# Loop for Champions League seasons, in this case the last 3 seasons
seasons = ['2022/2023', '2021/2022', '2020/2021']
dfs = []

for i in seasons:
    seasons_dropdown = driver.find_element(By.ID, 'seasons')
    seasons_select = Select(seasons_dropdown)
    seasons_select.select_by_visible_text(i)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Team Statistics"))
    )

    stats = driver.find_element(By.LINK_TEXT, "Team Statistics")
    stats.click()
    
    time.sleep(10)

    # Setting up BeautifulSoup
    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    # Scraping Summary table
    team_names = []
    goals = []
    shots_pgs = []
    yellow_cards = []
    red_cards = []
    possession_percs = []
    pass_percs = []
    aerials_wons = []
    ratings = []

    stats_content = soup.find('tbody', id='top-team-stats-summary-content')
    stats = stats_content.find_all('tr')

    for stat in stats:
        team_name = stat.find('a', class_='team-link').text.strip().split(". ")[1]
        goal = stat.find('td', class_='goal').text.strip()
        shots_pg = stat.find('td', class_='shotsPerGame').text.strip()
        yellow_card = stat.find('span', class_='yellow-card-box').text.strip()
        red_card = stat.find('span', class_='red-card-box').text.strip()
        possession_perc = stat.find('td', class_='possession').text.strip()
        pass_perc = stat.find('td', class_='passSuccess').text.strip()
        aerials_won = stat.find('td', class_='aerialWonPerGame').text.strip()
        rating = stat.find('span', class_='stat-value rating').text.strip()
        
        team_names.append(team_name)
        goals.append(goal)
        shots_pgs.append(shots_pg)
        yellow_cards.append(yellow_card)
        red_cards.append(red_card)
        possession_percs.append(possession_perc)
        pass_percs.append(pass_perc)
        aerials_wons.append(aerials_won)
        ratings.append(rating)

    # Creating DataFrames
    list = zip(team_names, goals, shots_pgs, yellow_cards, red_cards, possession_percs, pass_percs, aerials_wons, ratings)
    df = pd.DataFrame(list, columns=['team_names', 'goals', 'shots_pgs', 'yellow_cards', 'red_cards', 'possession_percs', 'pass_percs', 'aerials_won', 'ratings'])

    dfs.append(df)

    print(dfs)

time.sleep(10)

driver.quit()