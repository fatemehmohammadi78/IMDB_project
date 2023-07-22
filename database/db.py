from sqlalchemy import MetaData
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import json
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
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


def create_database():
    with engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {DB_NAME}"))


def show_database():
    with engine.connect() as conn:
        results = conn.execute(text('SHOW DATABASES;'))
        for res in results:
            return res


def show_tables():
    metadata = MetaData()
    metadata.reflect(engine)
    return metadata.tables.keys()


Base = declarative_base()


class Movie(Base):
    __tablename__ = "movie"

    id: Mapped[str] = mapped_column(String(8), primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    year: Mapped[int] = mapped_column(Integer)
    runtime: Mapped[int] = mapped_column(Integer)
    parental_guide: Mapped[str] = mapped_column(String(16))
    gross_us_canada: Mapped[int] = mapped_column(Integer)
    casts: Mapped["Cast"] = relationship(back_populates="movie")
    crews: Mapped["Crew"] = relationship(back_populates="movie")
    genres: Mapped["Genre"] = relationship(back_populates="movie")

    def __repr__(self) -> str:
        return f"Movie(id= {self.id}, Title= {self.title}, Year = {self.year}, Runtime = {self.Runtime}, Parental_Guide = {self.Parental_Guide}, Gross_US_Canada ={self.Gross_US_Canada} ) "


class Person(Base):
    __tablename__ = "person"

    id: Mapped[str] = mapped_column(String(8), primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    casts: Mapped["Cast"] = relationship(back_populates="person")
    crews: Mapped["Crew"] = relationship(back_populates="person")

    def __repr__(self) -> str:
        return f"Person(id= {self.id}, Name= {self.Name})"


class Cast(Base):
    __tablename__ = "cast"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[str] = mapped_column(String(8), ForeignKey("movie.id"))
    person_id: Mapped[str] = mapped_column(String(8), ForeignKey("person.id"))
    movie: Mapped["Movie"] = relationship(back_populates="casts")
    person: Mapped["Person"] = relationship(back_populates="casts")

    def __repr__(self) -> str:
        return f"Cast(id= {self.id}, Movie-id= {self.Movie_id}, Person_id = {self.Person_id})"


class Crew(Base):
    __tablename__ = "crew"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(String(8))
    movie_id: Mapped[str] = mapped_column(String(8), ForeignKey("movie.id"))
    person_id: Mapped[str] = mapped_column(String(8), ForeignKey("person.id"))
    movie: Mapped["Movie"] = relationship(back_populates="crews")
    person: Mapped["Person"] = relationship(back_populates="crews")

    def __repr__(self) -> str:
        return f"Cast(id= {self.id}, Movie-id= {self.Movie_id}, Person_id = {self.Person_id}, role = {self.role})"


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[str] = mapped_column(String(8), ForeignKey("movie.id"))
    genre: Mapped[str] = mapped_column(String(16))
    movie: Mapped["Movie"] = relationship(back_populates="genres")

    def __repr__(self) -> str:
        return f"Cast(id= {self.id}, Movie_id= {self.Movie_id}, genre = {self.genre})"


# Create tables:
Base.metadata.create_all(engine)

# Populate tables:
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
