# Movie Catalog

**CS178: Cloud and Database Systems — Project #1**
**Author:** Amber Lange
**GitHub:** AmberCaLa

---

## Overview

This project is a movie database. It allows users to search an existing database of movies. Users are also able to track movies they have completed along with their ratings of each movie.
<!-- Describe your project in 2-4 sentences. What does it do? Who is it for? What problem does it solve? -->

---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for movies
- **AWS DynamoDB** — non-relational database for movies completed by users
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py          # Main Flask application — routes and app logic
├── dbCode.py            # Database helper functions (MySQL connection + queries)
├── creds_sample.py      # Sample credentials file (see Credential Setup below)
├── templates/
│   ├── home.html        # Landing page
│   ├── [other].html     # Add descriptions for your other templates
├── .gitignore           # Excludes creds.py and other sensitive files
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/AmberCaLA/cs178-flask-app
   cd your-repo-name
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://54.146.202.127:8080
```

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

<!-- Briefly describe your relational database schema. What tables do you have? What are the key relationships? -->

**Example:**

- `movies` — stores movies ids, titles, release dates, and popularity; primary key is `movie_id`
- `movie_genres` — stores movie ids and genre ids; primary key is composite of `movie_id` and `genre_id`  
- `genre` — stores genre ids and corresponding genre names; primary key is to `genre_id`

The JOIN query used in this project: joined the `movies table` to the `movie_genres` table on `movie_id` then joined `movie_genres` table to `genre` table on `genre_id` to get every genre corresponding to each movie.

### DynamoDB

<!-- Describe your DynamoDB table. What is the partition key? What attributes does each item have? How does it connect to the rest of the app? -->

- **Table name:** `CompletedMovies`
- **Partition key:** `User`
- **Used for:** Storing the completed movies for each user and their rating for each movie

---

## CRUD Operations

| Operation | Route           | Description                                       |
| --------- | --------------- | ------------------------------------------------- |
| Create    | `/add-movie`    | Adds a movie to the database                      |  
| Read      | `/view-movies`  | Shows user first 50 movies in database            |
| Update    | `/update-movie` | Allows a user to update a movies popularity       |
| Delete    | `/delete-movie` | Allows a user to delete a movie from the database |

---

## Challenges and Insights

<!-- What was the hardest part? What did you learn? Any interesting design decisions? -->

---

## AI Assistance

<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here. -->
Used Claude to assist in generating a helper function to add movies to the database