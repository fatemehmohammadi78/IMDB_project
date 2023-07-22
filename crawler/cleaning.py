import json
import numpy as np


def get_data():
    with open('results.json', 'r') as f:
        data = json.load(f)
        return data


def fix_parental():
    data = get_data()
    for item in data:
        if not str(item['gross_us_canada']).isdigit():
            item['gross_us_canada'] = 0
        if not item['parental_guide'] or not item['parental_guide'].strip() or item['parental_guide'] == 'Not Rated':
            item['parental_guide'] = 'Unrated'

    with open('results.json', 'w') as f:
        json.dump(data, f, indent=4)


def person_items(movie_list):
    person_info = {}  # {id: name}
    for movie in movie_list:
        # star:
        for i in range(len(movie['stars'])):
            stars = movie['stars'][i]
            star_ids = movie['star_ids'][i]
            person_info[star_ids] = stars
        # writers:
        for i in range(len(movie['writers'])):
            writers = movie['writers'][i]
            writer_ids = movie['writer_ids'][i]
            person_info[writer_ids] = writers
        # directors:
        for i in range(len(movie['director'])):
            director = movie['director'][i]
            director_ids = movie['director_ids'][i]
            person_info[director_ids] = director

    return person_info


# print(person_items(get_data()))

def crew_items(movie_list):
    crew_list = []
    for movie in movie_list:
        for i in range(len(movie['director_ids'])):
            crew_item = {
                'movie_id': movie['movie_id'],
                'person_id': movie['director_ids'][i],
                'role': 'director',
            }
            crew_list.append(crew_item)
        for i in range(len(movie['writer_ids'])):
            crew_item = {
                'movie_id': movie['movie_id'],
                'person_id': movie['writer_ids'][i],
                'role': 'writer',
            }
            crew_list.append(crew_item)

    return crew_list


# print(crew_items())


def cast_items(movie_list):
    cast_info = []
    for movie in movie_list:
        for star_id in movie['star_ids']:
            res = {'movie_id': movie['movie_id'], 'person_id': star_id}
            cast_info.append(res)
    return cast_info


def movie_items(movie_list) -> list:
    movie_info = []
    for movie in movie_list:
        movie_item = {
            'id': movie['movie_id'] if movie['movie_id'] else None,
            'Title': movie['title'] if movie['title'] else None,
            'Year': movie['year'] if movie['year'] else None,
            'Runtime': movie['runtime'] if movie['runtime'] else None,
            'Parental_Guide': movie['parental_guide'] if str(movie['parental_guide']).lower() not in (
                np.nan, np.NAN, 'nan', 'NaN') else None,
            'Gross_US_Canada': movie['gross_us_canada'] if str(movie['gross_us_canada']).lower() not in (
                np.nan, np.NAN, 'nan', 'NaN') else None,
        }
        movie_info.append(movie_item)
    return movie_info


# print(movie_items(get_data()))


def genre_items(movie_list):
    genre_list = []
    for movie in movie_list:
        for genre in movie['genres']:
            genre_item = {
                'movie_id': movie['movie_id'],
                'genre': genre,
            }
        genre_list.append(genre_item)
    return genre_list
