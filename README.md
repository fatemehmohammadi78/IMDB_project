# IMDb Top 250 Movies Scraper and Dashboard

This project is a Python-based web scraping application that collects data from the top 250 IMDb movies and saves the information in a database using SQLAlchemy ORM. It also includes a Streamlit-powered dashboard for visualizing and exploring the collected data.

## Introduction

The IMDb Top 250 Movies Scraper and Dashboard is a project aimed at collecting essential information about the top 250 highest-rated movies on IMDb, including movie titles, directors, actors, and genres. The project utilizes web scraping techniques to extract data from IMDb's website, which is then saved into a MYSQL database using SQLAlchemy ORM for easy data management. Additionally, a Streamlit dashboard is provided to visualize the collected data and enable users to explore the movie details conveniently.


## Technologies

The project is built using the following technologies:

- Python 3.7+
- BeautifulSoup (for web scraping)
- Requests (for making HTTP requests)
- SQLAlchemy (for database operations)
- SQLite (database storage)
- Streamlit (for building the dashboard)

## Installation

To set up the project, follow these steps:

1. Clone the repository to your local machine:
git clone https://github.com/your-username/your-repo.git
cd your-repo

2. Create a virtual environment and activate it (optional but recommended):
python -m venv venv
source venv/bin/activate # For Windows: venv\Scripts\activate
3. Install the required dependencies:
pip install -r requirements.txt

4. Run the web scraping script to collect the movie data and store it in the database:
python scrape_imdb.py

5. Launch the Streamlit dashboard:
streamlit run dashboard.py


