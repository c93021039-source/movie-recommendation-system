import sqlite3
import re

conn = sqlite3.connect("movie.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    email TEXT PRIMARY KEY,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS genres(
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS movies(
    movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    genre_id INTEGER
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS ratings(
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    movie_id INTEGER,
    rating INTEGER
)
""")
conn.commit()
def check_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False
def add_user():
    name = input("Enter name: ")
    email = input("Enter email: ")
    if check_email(email):
        try:
            cursor.execute("""
            INSERT INTO users VALUES(?,?)
            """, (email, name))
            conn.commit()
            print("User Added")
        except:
            print("Email already exists")
    else:
        print("Invalid Email")
def add_genre():
    genre = input("Enter genre: ")
    cursor.execute("""
    INSERT INTO genres(genre_name)
    VALUES(?)
    """, (genre,))
    conn.commit()
    print("Genre Added")
def add_movie():
    title = input("Enter movie name: ")
    print("\nGenres")
    cursor.execute("SELECT * FROM genres")
    data = cursor.fetchall()
    for i in data:
        print(i)
    genre_id = int(input("Enter genre id: "))
    cursor.execute("""
    INSERT INTO movies(title, genre_id)
    VALUES(?,?)
    """, (title, genre_id))
    conn.commit()
    print("Movie Added")
def view_movies():
    cursor.execute("""
    SELECT movies.movie_id,
           movies.title,
           genres.genre_name
    FROM movies
    JOIN genres
    ON movies.genre_id = genres.genre_id
    """)
    data = cursor.fetchall()
    print("\nMovies List")
    for i in data:
        print(i)
def rate_movie():
    print("\nUsers")
    cursor.execute("SELECT * FROM users")
    for i in cursor.fetchall():
        print(i)
    email = input("Enter user email: ")
    cursor.execute("""
    SELECT * FROM users
    WHERE email = ?
    """, (email,))
    user = cursor.fetchone()
    if user == None:
        print("User not found")
        return
    print("\nMovies")
    cursor.execute("""SELECT movie_id,title FROM movies""")
    for i in cursor.fetchall():
        print(i)
    movie_id = int(input("Enter movie id: "))
    rating = int(input("Enter rating (1-5): "))
    if rating < 1 or rating > 5:
        print("Invalid Rating")
        return
    cursor.execute("""
    INSERT INTO ratings(user_email,movie_id,rating)
    VALUES(?,?,?)
    """, (email, movie_id, rating))
    conn.commit()
    print("Rating Added")
def top_movies():
    cursor.execute("""
    SELECT movies.title,
           AVG(ratings.rating)
    FROM ratings
    JOIN movies
    ON ratings.movie_id = movies.movie_id
    GROUP BY movies.movie_id
    ORDER BY AVG(ratings.rating) DESC
    """)
    data = cursor.fetchall()
    print("\nTop Rated Movies")
    for i in data:
        print(i)
def recommend_movies():
    cursor.execute("""
    SELECT movies.title,
           AVG(ratings.rating)
    FROM ratings
    JOIN movies
    ON ratings.movie_id = movies.movie_id
    GROUP BY movies.movie_id
    ORDER BY AVG(ratings.rating) DESC
    LIMIT 3
    """)
    data = cursor.fetchall()
    print("\nRecommended Movies")
    for i in data:
        print(i)
while True:
    print("""
===== MOVIE SYSTEM =====

1. Add User
2. Add Genre
3. Add Movie
4. View Movies
5. Rate Movie
6. Top Movies
7. Recommend Movies
8. Exit
""")
    choice = input("Enter Choice: ")
    if choice == "1":
        add_user()
    elif choice == "2":
        add_genre()
    elif choice == "3":
        add_movie()
    elif choice == "4":
        view_movies()
    elif choice == "5":
        rate_movie()
    elif choice == "6":
        top_movies()
    elif choice == "7":
        recommend_movies()
    elif choice == "8":
        print("Thank You")
        break
    else:
        print("Invalid Choice")
conn.close()