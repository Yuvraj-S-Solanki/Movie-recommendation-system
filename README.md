# 🎬 Movie Recommendation System

A content-based Movie Recommendation System built using Machine Learning and Streamlit. The application recommends movies similar to the one selected by the user and displays their posters using the TMDB API.

## 🚀 Live Demo

[Render deployment link here]

## 📌 Features

- Recommend top 5 similar movies
- Fetch movie posters from TMDB API
- Interactive and user-friendly Streamlit interface
- Content-based filtering using movie metadata
- Fast recommendation generation
- Responsive web application

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-Learn
- Pickle
- Requests
- TMDB API

## 📂 Project Structure

```text
Movie-recommendation-system/
│
├── app.py
├── movie_dict.pkl
├── similarity.pkl
├── requirements.txt
├── setup.sh
├── README.md
└── .gitattributes
```

## ⚙️ How It Works

1. User selects a movie from the dropdown list.
2. The system finds the selected movie in the dataset.
3. Similarity scores are calculated using a precomputed similarity matrix.
4. Top 5 most similar movies are recommended.
5. Movie posters are fetched dynamically from the TMDB API.
6. Recommendations are displayed with posters in the Streamlit interface.

## 🧠 Machine Learning Approach

This project uses **Content-Based Filtering**.

- Movie metadata such as genres, keywords, cast, crew, and overview are combined.
- Text data is converted into vectors.
- Cosine similarity is used to calculate similarity between movies.
- A similarity matrix is generated and stored for fast recommendations.

## 📸 Screenshots

### Home Page

<img width="1919" height="694" alt="image" src="https://github.com/user-attachments/assets/3cb6f90c-e61d-4387-82d2-d5a0913c83b9" />


### Recommendations

<img width="1919" height="904" alt="image" src="https://github.com/user-attachments/assets/67a7726f-83b8-4c05-8dce-c04336513b27" />

## 🔑 TMDB API

Movie posters are fetched using The Movie Database (TMDB) API.

Official Website:
https://www.themoviedb.org/

## 📈 Future Improvements

- Hybrid recommendation system
- User authentication
- Movie trailers integration
- Search functionality
- Personalized recommendations
- Deployment on AWS
