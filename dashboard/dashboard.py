import plotly.express as px
from sqlalchemy import create_engine, URL, func
from sqlalchemy.orm import sessionmaker
from models import Movie, Crew, Cast, Genre, Person
import pandas as pd
import streamlit as st

# Configuring Streamlit
st.set_page_config(
    page_title="IMDb Top 250 Movies",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def header():
    st.image('IMDb_Header_Page.jpg')
    st.write('## IMDb Top 250 Movies')


header()
DB_NAME = 'IMDb_database'

url_object = URL.create(
    "mysql+mysqlconnector",
    username="root",
    password="suramii78",
    host="localhost",
    database=DB_NAME,
)

engine = create_engine(url_object)
Session = sessionmaker(bind=engine)
session = Session()

# Filtering
# first part
with st.expander('Filter by Production Year'):
    start_year, end_year = st.slider('Select a range of production years', min_value=1997, max_value=2021,
                                     value=(1997, 2021))
    movies_year = session.query(Movie).filter(Movie.year.between(start_year, end_year)).all()

    movies_year_data = [
        {'id': movie.id, 'title': movie.title, 'year': movie.year, 'runtime': movie.runtime,
         'parental_guide': movie.parental_guide, 'gross_us_canada': movie.gross_us_canada} for
        movie in movies_year]
    movies_df = pd.DataFrame(movies_year_data)
    st.table(movies_df)

with st.expander('Filter by Duration'):
    start_duration, end_duration = st.slider('Select a duration range:', min_value=80, max_value=120,
                                             value=(80, 120))
    movies_duration = session.query(Movie).filter(Movie.runtime.between(start_duration, end_duration)).all()

    movies_duration_data = [
        {'id': movie.id, 'title': movie.title, 'year': movie.year, 'runtime': movie.runtime,
         'parental_guide': movie.parental_guide, 'gross_us_canada': movie.gross_us_canada} for
        movie in movies_duration]
    movies_df = pd.DataFrame(movies_duration_data)
    st.table(movies_df)

with st.expander('Filter by Actor'):
    selected_actors = st.multiselect('Select actor names:',
                                     options=[actor.name for actor in session.query(Person).all()])
    if len(selected_actors) > 0:
        movies_actor = session.query(Movie).join(Movie.casts).join(Cast.person). \
            filter(Person.name.in_(selected_actors)).all()

        movies_actor_data = [
            {'id': movie.id, 'title': movie.title, 'year': movie.year, 'runtime': movie.runtime,
             'parental_guide': movie.parental_guide, 'gross_us_canada': movie.gross_us_canada} for
            movie in movies_actor]
        movies_df = pd.DataFrame(movies_actor_data)
        st.table(movies_df)
    else:
        st.warning('Please select at least one actor.')

with st.expander('Filter by Genre'):
    genre_options = [genre[0] for genre in session.query(Genre.genre).distinct().all()]
    selected_genre = st.selectbox('Select a genre:', options=genre_options)

    if selected_genre:
        movies_genre = session.query(Movie).join(Movie.genres).filter(Genre.genre == selected_genre).all()

        movies_genre_data = [
            {'id': movie.id, 'title': movie.title, 'year': movie.year, 'runtime': movie.runtime,
             'parental_guide': movie.parental_guide, 'gross_us_canada': movie.gross_us_canada} for
            movie in movies_genre]
        movies_df = pd.DataFrame(movies_genre_data)
        st.table(movies_df)
    else:
        st.warning('Please select a genre.')

# second part
with st.expander('Visualizing the top 10 best-selling movies as a bar chart'):
    movies_top10 = session.query(Movie).order_by(Movie.gross_us_canada.desc()).limit(10).all()
    movie_titles = [movie.title for movie in movies_top10]
    movie_revenues = [movie.gross_us_canada for movie in movies_top10]

    movie_data = {'title': movie_titles, 'revenue': movie_revenues}
    movies_df = pd.DataFrame(data=movie_data)

    st.bar_chart(movies_df.set_index('title'), use_container_width=True)

with st.expander('Visualizing the 5 most active actors as a bar chart'):
    actors = session.query(Person.name, func.count(Cast.id)).join(Cast).group_by(Person.id).order_by(
        func.count(Cast.id).desc()).limit(5).all()
    df = pd.DataFrame(actors, columns=['Actor', 'Number of Appearances'])
    st.bar_chart(df.set_index('Actor'), width=200, height=500, use_container_width=True)

with st.expander('Visualizing the number of different genres as a pie chart'):
    genres = session.query(Genre.genre, func.count(Genre.id)).group_by(Genre.genre).all()
    df = pd.DataFrame(genres, columns=['Genre', 'Count'])
    fig = px.pie(df, values='Count', names='Genre')
    st.plotly_chart(fig)

with st.expander('Visualizing the number of age ratings for movies as a pie chart'):
    parental_guides = session.query(Movie.parental_guide).all()
    df = pd.DataFrame(parental_guides, columns=['Parental Guide'])
    counts = df['Parental Guide'].value_counts()
    fig = px.pie(counts, values=counts, names=counts.index.tolist(),
                 title='Number of Age Ratings of Movies')
    st.plotly_chart(fig)

with st.expander('Visualizing the top-grossing movies in the selected genre as a bar chart'):
    genres = session.query(Genre.genre).distinct().all()
    genre_list = [genre[0] for genre in genres]

    selected_genre = st.selectbox("Select a genre", genre_list)

    query = session.query(Movie.title, func.sum(Movie.gross_us_canada)). \
        join(Movie.genres). \
        filter(Genre.genre == selected_genre). \
        group_by(Movie.id). \
        order_by(func.sum(Movie.gross_us_canada).asc()).limit(20)
    movies = query.all()

    df = pd.DataFrame(data=movies, columns=['Title', 'Gross US Canada'])
    df['Gross US Canada'] = df['Gross US Canada'].astype(float)

    st.bar_chart(df.set_index('Title'))
