import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load movie dataset
def load_movies():
    return pd.read_csv("movies.csv")


# Create the recommendation model
def create_model(data):
    # Combine genre and description
    data["features"] = (
        data["genre"].fillna("") + " " +
        data["description"].fillna("")
    )

    # Convert text into numerical vectors
    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform(data["features"])

    # Calculate similarity between movies
    similarity = cosine_similarity(vectors)

    return similarity


# Get movie recommendations
def recommend_movies(movie_title, data, similarity, number=5):

    if movie_title not in data["title"].values:
        return []

    movie_index = data[data["title"] == movie_title].index[0]

    similarity_scores = list(enumerate(similarity[movie_index]))

    # Sort movies by similarity
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    # Skip the selected movie itself
    for index, score in similarity_scores[1:number + 1]:
        recommendations.append({
            "title": data.iloc[index]["title"],
            "genre": data.iloc[index]["genre"],
            "description": data.iloc[index]["description"],
            "score": round(float(score) * 100, 1)
        })

    return recommendations