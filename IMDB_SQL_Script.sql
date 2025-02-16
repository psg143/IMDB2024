CREATE DATABASE IMDB;

USE IMDB;
  
CREATE TABLE tblMovies
(
MovieName varchar(200),
Genre varchar(20), 
Ratings decimal(18,2),
VotecountOrg varchar(20), 
DurationOrg varchar(20), 
Votecount int,
Duration int,
MovieID INT AUTO_INCREMENT PRIMARY KEY
);
 
 
SELECT *
FROM tblMovies
ORDER BY Ratings DESC, Votecount DESC
LIMIT 10;
 
WITH RankedMovies AS (
SELECT 
	Genre, 
	MovieName, 
	Ratings,
	ROW_NUMBER() OVER (PARTITION BY Genre ORDER BY Ratings DESC, MovieName ASC) AS rn
FROM tblMovies
)
SELECT Genre, MovieName, Ratings 
FROM RankedMovies 
WHERE rn = 1;
 
WITH MovieRanks AS (
    SELECT 
        MovieName, DurationOrg,
        Duration,
        RANK() OVER (ORDER BY Duration ASC) AS shortest_rank,
        RANK() OVER (ORDER BY Duration DESC) AS longest_rank
    FROM tblMovies WHERE Duration>0
)
SELECT 'Shortest' AS Type, MovieName, DurationOrg, Duration FROM MovieRanks WHERE shortest_rank = 1
UNION ALL
SELECT 'Longest' AS Type, MovieName, DurationOrg, Duration FROM MovieRanks WHERE longest_rank = 1;
