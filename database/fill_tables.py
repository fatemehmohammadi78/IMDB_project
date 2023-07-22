import json
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from models import Movie, Person, Cast, Crew, Genre
from crawler.cleaning import movie_items, person_items, cast_items, genre_items, crew_items

DB_NAME = 'IMDb_database'

url_object = URL.create(
    "mysql+mysqlconnector",
    username="root",
    password="suramii78",
    host="localhost",
    database=DB_NAME

)

engine = create_engine(url_object)
Session = sessionmaker(bind=engine)
session = Session()

with open('..\\crawler\\results.json', 'r') as f:
    data = json.load(f)

# Movie
movies = [Movie(id=m['id'], title=m['Title'], year=m['Year'], runtime=m['Runtime'], parental_guide=m['Parental_Guide'],
                gross_us_canada=m['Gross_US_Canada'], ) for m in movie_items(data)]
session.add_all(movies)

# Person
person_dict = person_items(data)
person_list = [Person(id=k, name=person_dict[k]) for k in person_dict.keys()]
session.add_all(person_list)

# Crew
crew_list = [Crew(role=c['role'], movie_id=c['movie_id'], person_id=c['person_id']) for c in crew_items(data)]
session.add_all(crew_list)

# Cast
casts = [Cast(movie_id=c['movie_id'], person_id=c['person_id']) for c in cast_items(data)]
session.add_all(casts)

# Genre
genres = [Genre(movie_id=g['movie_id'], genre=g['genre']) for g in genre_items(data)]
session.add_all(genres)

session.commit()
