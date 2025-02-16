The IMDB 2024 Data Scraping and Visualizations project aims to extract and analyze movie data from IMDb for the year 2024. 
This project involves leveraging Selenium for web scraping, Pandas for data processing, SQL for structured storage, and Streamlit for interactive visualization. 
The primary goal is to identify trends in movie ratings, voting counts, and genre popularity, providing users with insights into the current movie landscape.
This project is particularly useful for entertainment analysts, movie enthusiasts, and data scientists who wish to explore IMDb movie statistics interactively.


Step 1: Web Scraping with Selenium
Used Selenium WebDriver to navigate the IMDb 2024 movie list.
Extracted key details such as Movie Name, Genre, Ratings, Voting Counts, and Duration.
Implemented explicit waits to handle dynamic page loading.
Pagination handling ensured that data across multiple pages was captured.
Stored extracted data temporarily in CSV files before merging them into a structured dataset.

Step 2: Data Storage in SQL
Created a normalized database schema for efficient querying.
Used SQLAlchemy ORM to manage database operations.
Imported cleaned CSV data into MySQL, ensuring indexing for faster access.
Used SQL queries to validate data integrity and eliminate duplicates.

Step 3: Data Analysis & Visualization with Streamlit
Designed a Streamlit dashboard for real-time data exploration.
Created multiple interactive visualizations, including: 
Top 10 Movies by Ratings and Votes (Bar chart)
Genre Distribution (Pie chart)
Average Movie Duration by Genre (Horizontal bar chart)
Rating Distribution (Histogram)
Voting Trends (Line chart)
Genre vs. Ratings Heatmap
Shortest and Longest Movies (Tabular view)
Integrated interactive filters to allow users to refine data dynamically based on: 
Duration (Short, Medium, Long)
Rating Threshold (Above a certain IMDb rating)
Voting Count (Popularity based filtering)
Genre Selection
