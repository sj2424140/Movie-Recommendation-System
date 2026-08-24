# 🎬 Movie Recommendation System

A web-based **Movie Recommendation System** built using Python, Streamlit, and Machine Learning. The application recommends movies similar to a movie selected by the user based on its **genre and description**.

The system uses **TF-IDF Vectorization** to convert movie descriptions and genres into numerical vectors and **Cosine Similarity** to find movies with similar content.

---

## 📌 Project Overview

Finding a movie to watch can be difficult when there are thousands of choices available.

This project provides a simple and interactive movie discovery platform where users can:

* 🔐 Create an account and log in
* 🎬 Search and select movies
* 🤖 Get similar movie recommendations
* 📊 View recommendation match scores
* 🖼️ View movie posters
* ⭐ Add recommended movies to favorites
* 🔎 Browse and search the movie collection
* 📖 Learn about the recommendation system through the About page

---

## ✨ Features

### 🔐 User Authentication

* User registration
* User login
* Password-protected accounts
* Local SQLite database for user information

### 🎬 Movie Recommendation

The system recommends movies based on:

* Movie genre
* Movie description
* Text similarity between movies

### 🤖 Machine Learning

The recommendation engine uses:

* **TF-IDF (Term Frequency–Inverse Document Frequency)**
* **Cosine Similarity**

These techniques identify movies whose textual features are most similar to the selected movie.

### 🖼️ Movie Posters

Movie posters are retrieved dynamically using the **IMDb suggestion API**.

### 🔎 Discover Page

Users can:

* Search movies by title
* Browse available movies
* Select a movie
* Generate recommendations

### ⭐ Favorites

Users can mark recommended movies as favorites during their session.

---

## 🧠 How the Recommendation System Works

The recommendation process follows these steps:

```text
                Movie Dataset
                     │
                     ▼
              movies.csv
                     │
                     ▼
          Combine Genre + Description
                     │
                     ▼
             TF-IDF Vectorizer
                     │
                     ▼
              Text Vectors
                     │
                     ▼
           Cosine Similarity
                     │
                     ▼
        Similarity Scores for Movies
                     │
                     ▼
       Sort Movies by Similarity
                     │
                     ▼
       Display Top 5 Recommendations
```

### Step 1 — Load Dataset

The application loads movie information from:

```text
movies.csv
```

The dataset contains movie titles, genres, and descriptions.

### Step 2 — Create Features

Genre and description are combined into a single text feature.

### Step 3 — TF-IDF Vectorization

TF-IDF converts the text into numerical vectors.

### Step 4 — Cosine Similarity

Cosine similarity measures how similar two movie vectors are.

### Step 5 — Generate Recommendations

The system sorts movies according to their similarity score and returns the top 5 similar movies.

---

## 🛠️ Technologies Used

| Technology          | Purpose                      |
| ------------------- | ---------------------------- |
| Python              | Core programming language    |
| Streamlit           | Web application interface    |
| Pandas              | Dataset handling             |
| Scikit-learn        | Machine Learning             |
| TF-IDF              | Text feature extraction      |
| Cosine Similarity   | Movie similarity calculation |
| SQLite              | User authentication database |
| Requests            | API requests                 |
| IMDb Suggestion API | Movie poster retrieval       |
| Git & GitHub        | Version control              |

---

## 📂 Project Structure

```text
Movie-Recommendation-System/
│
├── app.py
├── auth.py
├── recommender.py
├── movies.csv
├── test_tmdb.py
├── .gitignore
├── README.md
│
└── .streamlit/
    └── secrets.toml
```

> `secrets.toml` is intentionally excluded from GitHub because it contains private configuration/API credentials.

---

## 📄 File Description

### `app.py`

Main Streamlit application.

It handles:

* User interface
* Login and registration screens
* Movie selection
* Recommendations
* Movie posters
* Discover page
* About page
* Favorites

### `recommender.py`

Contains the recommendation engine.

Main functions:

```python
load_movies()
create_model()
recommend_movies()
```

### `auth.py`

Handles:

* User database initialization
* User registration
* User login

### `movies.csv`

Contains the movie dataset used by the recommendation engine.

### `test_tmdb.py`

Used for testing API connectivity/configuration.

### `.gitignore`

Prevents sensitive and unnecessary files from being uploaded to GitHub.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sj2424140/Movie-Recommendation-System.git
```

Move into the project directory:

```bash
cd Movie-Recommendation-System
```

### 2. Install Required Packages

Install the required Python libraries:

```bash
pip install streamlit pandas scikit-learn requests
```

If a `requirements.txt` file is added later, dependencies can be installed using:

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

The project uses Streamlit secrets for private configuration.

Create:

```text
.streamlit/secrets.toml
```

Do **not** upload this file to GitHub.

Keep private API credentials inside this file.

---

## ▶️ Running the Application

Run the Streamlit application using:

```bash
python -m streamlit run app.py
```

The application will normally open at:

```text
http://localhost:8501
```

---

## 🖥️ Application Pages

### 🔐 Login / Registration

Users can create an account and sign in before using the application.

### 🏠 Home

Users select a movie and click:

**Find Similar Movies**

The system then displays five recommended movies.

### 🔎 Discover

Users can search and browse movies available in the dataset.

### ℹ️ About

Provides information about the recommendation engine and technologies used in the project.

---

## 📸 Screenshots

Screenshots can be added to this section after creating a `screenshots` folder.

Example:

```markdown
## 📸 Screenshots

### Login Page

![Login Page](screenshots/login.png)

### Home Page

![Home Page](screenshots/home.png)

### Movie Recommendations

![Recommendations](screenshots/recommendations.png)

### Discover Page

![Discover Page](screenshots/discover.png)

### About Page

![About Page](screenshots/about.png)
```

---

## 🎯 Advantages

* Simple and user-friendly interface
* Content-based recommendation approach
* No requirement for user rating history
* Fast recommendation generation after model creation
* Interactive Streamlit interface
* Movie posters improve the visual experience

---

## ⚠️ Limitations

* Recommendations depend on the quality of movie descriptions and genres.
* The system is content-based and does not currently use collaborative filtering.
* New users do not have personalized recommendations based on their historical viewing behavior.
* Poster availability depends on the external IMDb suggestion service.
* The application currently uses a local SQLite database for authentication.

---

## 🚀 Future Enhancements

Possible improvements include:

* ⭐ User rating system
* ❤️ Persistent favorite movies
* 👤 Personalized recommendations based on user history
* 🔥 Trending movie recommendations
* 🎭 Genre-based filtering
* 📅 Movie release-date filtering
* 🌐 Deployment to Streamlit Cloud
* 🗄️ Cloud database integration
* 🎯 Hybrid recommendation system
* 📊 Recommendation analytics

---

## 🎓 Academic Project

**Project Title:** Movie Recommendation System

**Domain:** Machine Learning / Web Application

**Technology:** Python, Streamlit, Scikit-learn

**Recommendation Technique:** Content-Based Filtering

**Algorithms/Techniques:**

* TF-IDF Vectorization
* Cosine Similarity

---

## 👩‍💻 Author

**Sakshi Jadhav**

Computer Science & Engineering

---


