import streamlit as st
import pymysql
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def connect_to_database():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="abcd",
        database="IMDB",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

def fetch_movie_data(query):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(data)

    return df

def get_unique_values(df, column):
    return sorted(df[column].unique().tolist())

def main():
    st.title("IMDB Data Analysis")
    
    query = """SELECT * FROM tblMovies"""

    df = fetch_movie_data(query)
    
    df['Ratings'].fillna(df['Ratings'].mode(), inplace=True)
    df['Votecount'].fillna(df['Votecount'].mode(), inplace=True)
    df['Duration'].fillna(df['Duration'].mode(), inplace=True)
    df['Ratings'] = pd.to_numeric(df['Ratings'], errors='coerce')
    df['Votecount'] = pd.to_numeric(df['Votecount'], errors='coerce') 
    df['Genre'] = df['Genre'].str.upper()

    st.sidebar.header("Filters")
    genres = ["All"] + get_unique_values(df, "Genre")
    selected_genre = st.sidebar.selectbox("Select Genre", genres)

    Duration_range = st.sidebar.slider(
        "Duration (Minutes)",
        float(df["Duration"].min()),
        float(df["Duration"].max()),
        (float(df["Duration"].min()), float(df["Duration"].max()))
    )

    rating_range = st.sidebar.slider(
        "Star Rating",
        float(df["Ratings"].min()),
        float(df["Ratings"].max()),
        (float(df["Ratings"].min()), float(df["Ratings"].max()))
    )

    votecount_range = st.sidebar.slider(
        "Voting Counts",
        int(df["Votecount"].min()),
        int(df["Votecount"].max()),
        (int(df["Votecount"].min()), int(df["Votecount"].max()))
    )

    filtered_df = df.copy()

    if selected_genre != "All":
        filtered_df = filtered_df[filtered_df["Genre"] == selected_genre]

    filtered_df = filtered_df[
        (filtered_df["Ratings"] >= rating_range[0]) &
        (filtered_df["Ratings"] <= rating_range[1]) &
        (filtered_df["Votecount"] >= votecount_range[0]) &
        (filtered_df["Votecount"] <= votecount_range[1]) &
        (filtered_df["Duration"] >= Duration_range[0]) &
        (filtered_df["Duration"] <= Duration_range[1])
    ]

    st.header("Filtered Results")
    st.write(f"Found {len(filtered_df)} movies matching your criteria")

    st.dataframe(
        filtered_df[[
            "MovieName", "Genre", "Ratings", "VotecountOrg",
            "DurationOrg", "Votecount", "Duration"
        ]],
        hide_index=True
    )

    ######################### Top 10 Movies by Rating and Voting Counts ############################
    sorted_df = df.sort_values(by=['Ratings', 'Votecount'], ascending=[False, False])

    top_10_df = sorted_df.head(10)

    st.header("Top 10 Movies by Rating and Voting Counts")
    st.dataframe(top_10_df,hide_index=True)

    ######################### Genre Distribution ###################################################
    st.header("Genre Distribution")
    Genregrouped_df = df.groupby(['Genre'])[['MovieID']].count()
    Genregrouped_df = Genregrouped_df.rename(columns={'Genre': 'Genre', 'MovieID': 'Count'})

    plt.figure(figsize=(10, 6))
    sns.barplot(data=Genregrouped_df,x='Genre',y='Count')
    st.pyplot(plt)

    ######################### Average Duration by Genre #############################################
    st.header("Average Duration by Genre")
    GenreAvg_df = df.groupby(['Genre'])[['Duration']].mean().round(0)
    GenreAvg_df = GenreAvg_df.rename(columns={'Genre': 'Genre', 'Duration': 'Duration(in Minutes)'})

    plt.figure(figsize=(10, 6))
    sns.barplot(data=GenreAvg_df, x="Duration(in Minutes)", y="Genre", orient = 'h')
    st.pyplot(plt)

    ######################### Voting Trends by Genre #############################################
    st.header("Voting Trends by Genre")
    plt.figure(figsize=(10, 6))
    ax = sns.swarmplot(x='Genre', y='Votecount', data=df)
    mean_values = df.groupby('Genre')['Votecount'].mean()

    for index, day in enumerate(mean_values.index):
        plt.axhline(mean_values[day], color='purple', linestyle='-', linewidth=3, alpha=0.5)

    st.pyplot(plt)

    ######################### Rating Distribution #############################################
    st.header("Rating Distribution")
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df,x='Ratings')
    st.pyplot(plt)

    ######################### Genre-Based Rating Leaders #############################################
    st.header("Genre-Based Rating Leaders")
    
    trquery = """WITH RankedMovies AS (
        SELECT
            Genre,
            MovieName,
            Ratings,
            ROW_NUMBER() OVER (PARTITION BY Genre ORDER BY Ratings DESC, MovieName ASC) AS rn
        FROM tblMovies
        )
        SELECT UCASE(Genre) AS Genre, MovieName, Ratings
        FROM RankedMovies
        WHERE rn = 1"""

    dftr = fetch_movie_data(trquery)
    st.dataframe(dftr,hide_index=True)

    ######################### Most Popular Genres by Voting #############################################
    st.header("Most Popular Genres by Voting")
    GenreAvgvc1_df = df.groupby(['Genre'])[['Votecount']].sum()
    GenreAvgvc1_df = GenreAvgvc1_df.rename(columns={'Genre': 'Genre', 'Votecount': 'Votecount'})
    plt.figure(figsize=(8, 4))
    GenreAvgvc1_df.plot(kind='pie', y='Votecount', autopct='%1.0f%%') 
    st.pyplot(plt)

    # st.dataframe(GenreAvgvc1_df,hide_index=False)

    ######################### Duration Extremes #############################################
    st.header("Duration Extremes")

    trquery = """WITH MovieRanks AS (
            SELECT 
                MovieName, DurationOrg, Duration,
                RANK() OVER (ORDER BY Duration ASC) AS shortest_rank,
                RANK() OVER (ORDER BY Duration DESC) AS longest_rank
            FROM tblMovies WHERE Duration>0
        )
        SELECT 'Shortest' AS Type, MovieName, DurationOrg, Duration FROM MovieRanks WHERE shortest_rank = 1
        UNION ALL
        SELECT 'Longest' AS Type, MovieName, DurationOrg, Duration FROM MovieRanks WHERE longest_rank = 1;"""

    dfsl = fetch_movie_data(trquery)
    st.dataframe(dfsl,hide_index=True)

    ######################### Ratings by Genre #############################################
    st.header("Ratings by Genre")
    GenreAvgrd1_df = df.groupby(['Genre'])[['Ratings']].mean().round(1)
    GenreAvgrd1_df = GenreAvgrd1_df.rename(columns={'Genre': 'Genre', 'Ratingst': 'Ratingsnt'})

    # st.dataframe(GenreAvgrd1_df,hide_index=False)
    plt.figure(figsize=(10, 6))
    sns.heatmap(GenreAvgrd1_df, annot=True)
    st.pyplot(plt)

    ######################### Correlation Analysis #############################################
    st.header("Correlation Analysis")

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="Ratings", y="Votecount")
    st.pyplot(plt)


if __name__ == "__main__":
    main()
