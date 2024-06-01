import requests as re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pymongo
import concurrent.futures
import json
import logging
import streamlit as st
from streamlit_option_menu import option_menu

# Configure logging
logging.basicConfig(
    filename='scraping.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def beautify_strs(strings):
    new_strings = []
    for string in strings:
        string = string.replace('\n', '')
        string = string.replace('  ', '')
        new_strings.append(string)
    return new_strings


def beautify_str(string):
    if string is None:
        return "N/A"
    string = string.replace('\n', '').replace('  ', '')
    return string


def scrap_heading(url):
    try:
        response = re.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        heading = soup.find('h1')
        logging.info(f'Successfully scraped heading from {url}')

        return heading.text

    except Exception as e:
        logging.error(f'Error scraping heading from {url}: {e}')

        return "Heading not available"


def scrap_description(url):
    try:
        response = re.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        description = soup.find('p', attrs={'class': 'lead'})

        logging.info(f'Successfully scraped description from {url}')
        return description.text.strip()

    except Exception as e:
        logging.error(f'Error scraping description from {url}: {e}')
        return "Error fetching description."

def scrap_last(url):
    try:
        content = []

        response = re.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        heading = soup.find('h3')
        content.append(heading.text)

        des1 = soup.find('p', attrs={'class': 'lead'})
        content.append(beautify_str(des1.text))

        scraper = soup.find_all('h4')
        paragraphs = soup.find_all('p')[1:]

        for i in range(len(scraper)):
            anchor = scraper[i].find('a')
            des2 = paragraphs[i].text

            content.append(beautify_str(anchor.text))
            content.append(beautify_str(des2))

        logging.info(f'Successfully scraped content from {url}')

        return content

    except Exception as e:
        logging.error(f'Error scraping content from {url}: {e}')
        return "Error scraping content."
def scrap_tables(url):
    try:
        html_open = open(url, "r")
        contents = html_open.read()

        soup = BeautifulSoup(contents, 'html.parser')
        table_head = soup.find('thead')
        table_body = soup.find("tbody")

        headers = table_head.find_all("th")
        titles = []

        for header in headers:
            header_title = header.text
            titles.append(header_title)

        titles = beautify_strs(titles)

        rows = table_body.find_all("tr")
        arr = []

        for row in rows:
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            arr.append(cols)

        arr_n = np.array(arr).T
        arr_n[3, 0] = 1

        data_dict = {}

        for x in range(len(titles)):
            data_dict[titles[x]] = arr_n[x]

        df = pd.DataFrame(data_dict)

        logging.info(f'Successfully scraped tables from {url}')

        return df

    except Exception as e:
        logging.error(f'Error scraping tables from {url}: {e}')

        return pd.DataFrame()


def hockeyscraper(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='table')

        headers = table.find_all('th')
        titles = []

        for header in headers:
            header_title = header.text
            titles.append(header_title)

        titles = beautify_strs(titles)

        body = table.find_all('tr', class_='team')
        hockey = []

        for row in body:
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            cols = beautify_strs(cols)
            hockey.append(cols)

        hockey = np.array(hockey).T
        dict_hockey = dict(zip(titles, hockey))
        df = pd.DataFrame(dict_hockey)

        logging.info(f'Successfully scraped hockey data from {url}')

        return df

    except Exception as e:
        logging.error(f'Error scraping hockey data from {url}: {e}')

        return pd.DataFrame()


def movies_data(year):
    url = f'scraping{year}.html'
    df = scrap_tables(url)

    try:
        for idx, group in df.groupby(np.arange(len(df)) // df.shape[0]):
            group.to_json(f'{year}_movies.json', orient='index')

        with open(f'{year}_movies.json', 'r') as f:
            data = json.load(f)

        client = pymongo.MongoClient('mongodb://localhost:27017/')

        db = client[f'movies_{year}']
        info = db.movies_sample

        data_values = data.values()
        info.insert_many(data_values)

        logging.info(f'Successfully saved movies data for {year} to MongoDB')

    except Exception as e:
        logging.error(f'Error saving movies data for {year} to MongoDB: {e}')


def scrape_hockey(num):
    url = f'https://www.scrapethissite.com/pages/forms/?page_num={num}'
    df = hockeyscraper(url)

    try:
        for idx, group in df.groupby(np.arange(len(df)) // df.shape[0]):
            group.to_json(f'hockey_{num}.json', orient='index')

        with open(f'hockey_{num}.json', 'r') as f:
            data = json.load(f)

        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client[f'hockey_{num}']

        info = db.hockey_sample
        data_values = data.values()
        info.insert_many(data_values)

        logging.info(f'Successfully saved hockey data for page {num} to MongoDB')

    except Exception as e:
        logging.error(f'Error saving hockey data for page {num} to MongoDB: {e}')


def all_movies():
    years = np.arange(2010, 2016)

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            executor.map(movies_data, years)

        logging.info('Successfully scraped and saved all movies data')

    except Exception as e:
        logging.error(f'Error scraping and saving all movies data: {e}')


def all_hockey():
    pages = np.arange(1, 25)

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
            executor.map(scrape_hockey, pages)

        logging.info('Successfully scraped and saved all hockey data')

    except Exception as e:
        logging.error(f'Error scraping and saving all hockey data: {e}')


def front_end_selector1():
    option = st.selectbox("Which year Data do you need?", np.arange(2010, 2016))

    url = f'https://www.scrapethissite.com/pages/ajax-javascript/#{option}'
    local_url = f'scraping{option}.html'
    df = scrap_tables(local_url)

    st.title(beautify_str(scrap_heading(url)))
    description = beautify_str(scrap_description(url))
    st.write(description)
    st.write(df)

def front_end_selector2():
    option = st.selectbox("Which page Data do you need?", np.arange(1, 25))

    url = f'https://www.scrapethissite.com/pages/forms/?page_num={option}'

    df = hockeyscraper(url)

    st.title(beautify_str(scrap_heading(url)))
    description = beautify_str(scrap_description(url))
    st.write(description)
    st.write(df)

def front_end_final():
    content = scrap_last(f'https://www.scrapethissite.com/pages/advanced/')

    i = 0
    while i < len(content) - 1:
        st.title(content[i])
        st.write(content[i+1])
        i += 2

def main():
    logging.info('Script started')

    # front_end_selector()
    # all_movies()
    # all_hockey()
    # front_end_selector2()

    with st.sidebar:
        select = option_menu("Select Page to Scrape",
                             ["Movies Data", "Hockey Data", "Pages Advanced"],
                             menu_icon="cast", default_index=0, orientation="horizontal")

    if select == 'Movies Data':
        front_end_selector1()

    elif select == 'Hockey Data':
        front_end_selector2()

    elif select == 'Pages Advanced':
        front_end_final()

    logging.info('Script finished')


if __name__ == "__main__":
    main()
