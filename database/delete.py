import json
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from models import Movie, Person, Cast, Crew, Genre, Base
from crawler.cleaning import movie_items, get_data, person_items
from crawler.cleaning import cast_items, get_data

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

Cast.__table__.drop(engine)
Crew.__table__.drop(engine)
Genre.__table__.drop(engine)
Person.__table__.drop(engine)
Movie.__table__.drop(engine)


# session.query(Cast).delete()
# session.query(Crew).delete()
# session.query(Genre).delete()
# session.query(Person).delete()
# session.query(Movie).delete()
#
#
# session.commit()
