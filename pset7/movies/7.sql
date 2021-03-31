SELECT title, rating FROM movies 
JOIN ratings ON movies.id = ratings.movie_id
WHERE year = 2010 AND rating > 0 ORDER BY rating DESC, title