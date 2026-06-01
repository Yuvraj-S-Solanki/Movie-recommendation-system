import pickle
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .stApp {
        background: linear-gradient(165deg, #0a0e17 0%, #12182a 45%, #0d1117 100%);
    }

    .hero h1 {
        font-size: clamp(2rem, 5vw, 3.2rem);
        font-weight: 700;
        margin: 0;
        text-align: center;
        background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcb77);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero p {
        text-align: center;
        color: #9ca3af;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
    }

    /* --- search panel only (screenshot area) --- */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.25rem 1.5rem 1.35rem;
        margin: 0 auto;
        max-width: 640px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    }

    .choose-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.9rem;
    }

    .choose-header img {
        width: 2.75rem;
        height: 2.75rem;
        object-fit: contain;
    }

    .choose-header span {
        color: #f8fafc;
        font-size: 1.45rem;
        font-weight: 700;
    }

    div[data-testid="stForm"] div[data-baseweb="select"] > div {
        background-color: #1a2332 !important;
        color: #f3f4f6 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        min-height: 2.75rem;
        font-size: 1rem !important;
    }

    div[data-testid="stForm"] div[data-baseweb="select"] input {
        color: #f3f4f6 !important;
        font-size: 1rem !important;
        -webkit-text-fill-color: #f3f4f6 !important;
    }

    div[data-testid="stForm"] div[data-baseweb="select"] input::placeholder {
        color: #d1dce8 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #d1dce8 !important;
    }

    div[data-testid="stForm"] div[data-baseweb="select"] > div > div {
        color: #f3f4f6 !important;
    }

    div[data-testid="stForm"] div[data-baseweb="select"] svg {
        fill: #9ca3af !important;
    }

    div[data-testid="stForm"] .stFormSubmitButton > button {
        width: 100%;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.5rem !important;
        background: linear-gradient(135deg, #e63946 0%, #ff4b4b 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 999px !important;
        height: 50px !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        margin-top: 0.35rem;
        box-shadow: 0 4px 18px rgba(255, 75, 75, 0.4) !important;
    }

    div[data-testid="stForm"] .stFormSubmitButton > button::before {
        content: "🚀";
        font-size: 1.15rem;
        filter: brightness(0) invert(1);
    }

    div[data-testid="stForm"] .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #ff4b4b 0%, #ff6666 100%) !important;
        box-shadow: 0 6px 22px rgba(255, 75, 75, 0.5) !important;
    }

    .loading-panel {
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 14px;
        padding: 1.1rem 1.25rem;
        margin: 1rem auto 0;
        max-width: 640px;
        text-align: center;
    }

    .loading-panel .loading-title {
        color: #f1f5f9;
        font-size: 1.05rem;
        font-weight: 600;
    }

    .loading-panel .loading-sub {
        color: #94a3b8;
        font-size: 0.88rem;
        margin-top: 0.25rem;
    }

    div[data-testid="stMain"] div[data-testid="stSpinner"],
    div[data-testid="stMain"] div[data-testid="stStatusWidget"] {
        display: none !important;
    }

    section[data-testid="stSidebar"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    .movie-card {
        background: linear-gradient(180deg, #1a2234 0%, #141b28 100%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 0.75rem;
        text-align: center;
        height: 100%;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }

    .movie-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.45);
        border-color: rgba(255, 107, 107, 0.25);
    }

    .movie-rank {
        display: inline-block;
        background: rgba(255, 107, 107, 0.2);
        color: #ff8a8a;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
        margin-bottom: 0.5rem;
    }

    .movie-title {
        color: #f9fafb;
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 0.65rem;
        line-height: 1.35;
        min-height: 2.6em;
    }

    .results-header {
        color: #f3f4f6;
        font-size: 1.35rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem;
        text-align: center;
    }

</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Requests Session
# --------------------------------------------------
session = requests.Session()

retry = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)

adapter = HTTPAdapter(max_retries=retry)

session.mount("http://", adapter)
session.mount("https://", adapter)


# --------------------------------------------------
# Fetch Poster
# --------------------------------------------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    api_key = "af5cd7148dbe9ddab09f4706808ea162"

    url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{movie_id}?api_key={api_key}&language=en-US"
    )

    try:
        response = session.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

    except Exception as e:
        print(f"Poster Error ({movie_id}): {e}")

    return "https://via.placeholder.com/500x750?text=No+Poster"


# --------------------------------------------------
# Recommendation Function
# --------------------------------------------------
def recommend(movie):
    try:
        index = movies[movies["title"] == movie].index[0]

        distances = sorted(
            list(enumerate(similarity[index])),
            reverse=True,
            key=lambda x: x[1],
        )

        recommended_movie_names = []
        recommended_movie_posters = []

        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id

            recommended_movie_names.append(movies.iloc[i[0]].title)

            poster = fetch_poster(movie_id)

            recommended_movie_posters.append(poster)

        return recommended_movie_names, recommended_movie_posters

    except Exception as e:
        st.error(f"Recommendation Error: {e}")

        return [], []


# --------------------------------------------------
# Load Data
# --------------------------------------------------
try:
    movies = pickle.load(open("movie_list.pkl", "rb"))

    similarity = pickle.load(open("similarity.pkl", "rb"))

except Exception as e:
    st.error(f"Error Loading Files: {e}")

    st.stop()


# --------------------------------------------------
# Header & Movie Selection
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🎬 Movie Recommender System</h1>
        <p>Find movies similar to your favorites</p>
    </div>
    """,
    unsafe_allow_html=True,
)

movie_list = movies["title"].values

_, center, _ = st.columns([1, 2, 1])

with center:
    with st.form("recommend_form", clear_on_submit=False):
        st.markdown(
            """
            <div class="choose-header">
                <img src="https://cdn-icons-png.flaticon.com/512/4221/4221484.png" alt="" />
                <span>Choose a movie</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        selected_movie = st.selectbox(
            "Choose a movie",
            movie_list,
            index=None,
            placeholder="Type to search the catalog…",
            label_visibility="collapsed",
        )

        show_recs = st.form_submit_button(
            "Show recommendations",
            type="primary",
            use_container_width=True,
        )

    loading_area = st.empty()


# --------------------------------------------------
# Recommendations
# --------------------------------------------------
if show_recs:
    if not selected_movie:
        st.warning("Please choose a movie from the list first.")
    else:
        loading_area.markdown(
            """
            <div class="loading-panel">
                <div class="loading-title">Finding similar movies… 🍿</div>
                <div class="loading-sub">Fetching posters from TMDB…</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        names, posters = recommend(selected_movie)

        loading_area.empty()

        if len(names) > 0:
            st.markdown(
                f'<p class="results-header">Because you liked <em>{selected_movie}</em></p>',
                unsafe_allow_html=True,
            )

            cols = st.columns(5, gap="medium")

            for i in range(min(5, len(names))):
                with cols[i]:
                    st.markdown(
                        f"""
                        <div class="movie-card">
                            <span class="movie-rank">#{i + 1}</span>
                            <img src="{posters[i]}" alt="{names[i]}"
                                 style="width:100%; border-radius:10px; margin-top:0.25rem;">
                            <p class="movie-title">{names[i]}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        else:
            st.warning("No recommendations found. Try another title.")
