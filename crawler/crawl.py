import json
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from urllib.parse import urljoin

initial_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9'
}
response = requests.get(initial_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
movie_links = soup.select('td.titleColumn > a')
movie_urls = [urljoin(initial_url, link.get('href')) for link in movie_links]

results = []
for url in movie_urls:
    try:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        result = {}
        title = soup.find('h1').text.strip()
        year = soup.select('.kNzJA-D li')[0].text.strip()
        try:
            parental_guide = soup.select('.kNzJA-D li')[1].text.strip()
        except:
            parental_guide = np.NAN
        runtime = soup.select('.kNzJA-D li')[2].text.strip()
        if re.match(r'^\d+h \d+m$', runtime):
            hours, minutes = runtime.split("h")
            minutes = minutes.replace('m', '')
            total_minutes = int(hours) * 60 + int(minutes)

        elif re.match(r'^(\d+)m$', runtime):
            total_minutes = int(runtime.replace('m', ''))

        else:
            hours = runtime.replace('h', '')
            total_minutes = int(hours) * 60

        genres = [genre.text.strip() for genre in soup.find_all('a', class_='ipc-chip ipc-chip--on-baseAlt')]
        first_div = soup.find('div', class_='ipc-metadata-list-item__content-container')
        second_div = first_div.find_next('div', class_='ipc-metadata-list-item__content-container')
        third_div = second_div.find_next('div', class_='ipc-metadata-list-item__content-container')
        directors = [director.text.strip() for director in first_div.find_all('a') if '/name/' in director.get('href')]
        writers = [writer.text.strip() for writer in second_div.find_all('a') if '/name/' in writer.get('href')]
        stars = [writer.text.strip() for writer in third_div.find_all('a') if '/name/' in writer.get('href')]
        movie_id = re.findall(r'tt(\d+)/', url)[0]
        director_ids = [re.findall(r'nm(\d+)/', director.get('href'))[0] for director in first_div.find_all('a') if
                        '/name/' in director.get('href')]
        writer_ids = [re.findall(r'nm(\d+)/', writer.get('href'))[0] for writer in second_div.find_all('a') if
                      '/name/' in writer.get('href')]
        star_ids = [re.findall(r'nm(\d+)/', star.get('href'))[0] for star in third_div.find_all('a') if
                    '/name/' in star.get('href')]
        try:
            box_office = soup.find_all(class_='sc-f65f65be-0 fVkLRr')[2].find_next('h3')
            box_office_ul = box_office.find_next('ul')
            gross = box_office_ul.find_all('li')[3].text
            gross = gross.replace('$', '').replace(',', '')
        except:
            gross = np.nan

        result['movie_id'] = movie_id
        result['title'] = title
        result['year'] = year
        result['parental_guide'] = parental_guide
        result['runtime'] = total_minutes
        result['genres'] = genres
        result['director'] = directors
        result['director_ids'] = director_ids
        result['writers'] = writers
        result['writer_ids'] = writer_ids
        result['stars'] = stars
        result['star_ids'] = star_ids
        result['gross_us_canada'] = gross
        results.append(result)
        print(result)
    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")

with open('results.json', 'w') as f:
    json.dump(results, f)
