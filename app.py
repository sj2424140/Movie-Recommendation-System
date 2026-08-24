import html
import streamlit as st
import requests

from recommender import load_movies, create_model, recommend_movies
from auth import init_db, register_user, login_user


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# DATABASE
# ============================================================

init_db()


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "logged_in": False,
    "username": "",
    "page": "Home",
    "selected_movie": "",
    "recommendations": [],
    "favorites": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(124, 58, 237, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 5%,
                rgba(239, 68, 68, 0.12),
                transparent 28%
            ),
            #07080c;

        color: white;
    }

    .block-container {
        max-width: 1350px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4 {
        color: white !important;
    }

    p {
        color: #b8bac5;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    .stButton > button {
        min-height: 44px;
        border-radius: 10px;
        font-weight: 650;
        border: 1px solid rgba(255,255,255,0.10);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: rgba(255,255,255,0.30);
    }

    .stTextInput input {
        border-radius: 10px;
    }

    div[data-baseweb="select"] {
        border-radius: 10px;
    }

    .brand {
        font-size: 21px;
        font-weight: 800;
        color: white;
        white-space: nowrap;
    }

    .hero-label {
        color: #a78bfa;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .hero-title {
        color: white;
        font-size: 50px;
        font-weight: 900;
        line-height: 1.08;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        color: #a6a8b3;
        font-size: 17px;
        line-height: 1.7;
        max-width: 820px;
    }

    .movie-name {
        color: white;
        font-size: 32px;
        font-weight: 850;
        margin-bottom: 7px;
    }

    .movie-genre {
        color: #a1a3af;
        font-size: 14px;
        margin-bottom: 18px;
    }

    .movie-description {
        color: #d2d3da;
        font-size: 15px;
        line-height: 1.75;
    }

    .section-label {
        color: #a78bfa;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .card-title {
        color: white;
        font-size: 18px;
        font-weight: 750;
        line-height: 1.3;
        margin-top: 10px;
        min-height: 48px;
    }

    .card-genre {
        color: #9699a6;
        font-size: 13px;
        margin: 4px 0 8px;
    }

    .card-description {
        color: #bfc1ca;
        font-size: 13px;
        line-height: 1.55;
        min-height: 62px;
    }

    .match-label {
        color: #858895;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 10px;
    }

    .match-value {
        color: white;
        font-size: 24px;
        font-weight: 850;
    }

    .poster-fallback {
        height: 420px;
        border-radius: 14px;

        background: linear-gradient(
            145deg,
            #191b24,
            #0d0e13
        );

        border: 1px solid rgba(255,255,255,0.08);

        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;

        text-align: center;
    }

    .poster-fallback-icon {
        font-size: 55px;
        margin-bottom: 10px;
    }

    .poster-fallback-text {
        color: #777b88;
        font-size: 13px;
    }

    .discover-title {
        color: white;
        font-size: 40px;
        font-weight: 850;
        margin-bottom: 5px;
    }

    .info-box {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 24px;
        min-height: 180px;
    }

    .info-title {
        color: white;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .info-text {
        color: #a6a8b3;
        font-size: 14px;
        line-height: 1.7;
    }

    .login-space {
        height: 7vh;
    }

    .login-logo {
        text-align: center;
        font-size: 58px;
        margin-bottom: 5px;
    }

    .login-title {
        text-align: center;
        font-size: 38px;
        font-weight: 850;
        margin-bottom: 6px;
    }

    .login-subtitle {
        text-align: center;
        color: #9ca0ad;
        font-size: 16px;
        margin-bottom: 28px;
    }

    .footer {
        text-align: center;
        color: #646875;
        font-size: 13px;
        padding: 30px 0 5px;
    }

    @media (max-width: 800px) {

        .hero-title {
            font-size: 34px;
        }

        .login-title {
            font-size: 28px;
        }

        .discover-title {
            font-size: 30px;
        }

        .brand {
            font-size: 16px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD MOVIE MODEL
# ============================================================

@st.cache_resource
def get_movie_model():

    movies = load_movies()

    similarity = create_model(movies)

    return movies, similarity


movies, similarity = get_movie_model()


# ============================================================
# MOVIE POSTER - IMDb
# ============================================================

from urllib.parse import quote


@st.cache_data(show_spinner=False, ttl=86400)
def get_poster(movie_name):
    """
    Get movie poster from IMDb.
    No TMDB API key is required.
    """

    if not movie_name:
        return None

    try:
        # IMDb suggestion API
        search_url = (
            "https://v3.sg.media-imdb.com/"
            "suggestion/titles/x/"
            + quote(str(movie_name))
            + ".json"
        )

        response = requests.get(
            search_url,
            timeout=5,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code != 200:
            return None

        data = response.json()

        results = data.get("d", [])

        if not results:
            return None

        # Find the best movie result with a poster
        for result in results:

            # Only accept movie-type results
            qid = result.get("qid", "")

            if qid not in [
                "movie",
                "tvMovie",
                "video"
            ]:
                continue

            image_data = result.get("i")

            if not image_data:
                continue

            # IMDb normally returns:
            # {"imageUrl": "...", "width": ..., "height": ...}

            if isinstance(image_data, dict):

                image_url = image_data.get("imageUrl")

                if image_url:
                    return image_url

        # If no movie-type result was found,
        # try any result that has an image.
        for result in results:

            image_data = result.get("i")

            if isinstance(image_data, dict):

                image_url = image_data.get("imageUrl")

                if image_url:
                    return image_url

        return None

    except requests.exceptions.Timeout:
        return None

    except requests.exceptions.ConnectionError:
        return None

    except requests.exceptions.RequestException:
        return None

    except Exception:
        return None


# ============================================================
# DISPLAY POSTER
# ============================================================

def show_poster(movie_name):

    poster_url = get_poster(movie_name)

    if poster_url:

        try:

            st.image(
                poster_url,
                use_container_width=True
            )

            return

        except Exception:
            pass

    # Poster unavailable fallback
    st.markdown(
        """
        <div class="poster-fallback">
            <div class="poster-fallback-icon">🎬</div>
            <div class="poster-fallback-text">
                Poster unavailable
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ============================================================
# LOGIN / REGISTER
# ============================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="login-space"></div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns(
        [1, 1.35, 1]
    )

    with center:

        st.markdown(
            '<div class="login-logo">🎬</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-title">'
            'Movie Recommendation System'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-subtitle">'
            'Discover movies you will love.'
            '</div>',
            unsafe_allow_html=True
        )

        login_tab, register_tab = st.tabs(
            [
                "🔐 Sign In",
                "✨ Create Account"
            ]
        )

        # ====================================================
        # LOGIN
        # ====================================================

        with login_tab:

            st.subheader("Welcome back")

            st.caption(
                "Sign in to continue discovering movies."
            )

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )

            st.write("")

            if st.button(
                "Sign In",
                type="primary",
                use_container_width=True,
                key="login_button"
            ):

                if not username or not password:

                    st.warning(
                        "Please enter your username and password."
                    )

                else:

                    result = login_user(
                        username.strip(),
                        password
                    )

                    if result:

                        st.session_state.logged_in = True

                        if isinstance(result, dict):

                            st.session_state.username = result.get(
                                "username",
                                username.strip()
                            )

                        else:

                            st.session_state.username = (
                                username.strip()
                            )

                        st.session_state.page = "Home"

                        st.rerun()

                    else:

                        st.error(
                            "Incorrect username or password."
                        )

        # ====================================================
        # REGISTER
        # ====================================================

        with register_tab:

            st.subheader(
                "Create your account"
            )

            st.caption(
                "Create an account to start discovering movies."
            )

            new_username = st.text_input(
                "Username",
                placeholder="Choose a username",
                key="register_username"
            )

            new_password = st.text_input(
                "Password",
                type="password",
                placeholder="Minimum 6 characters",
                key="register_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password",
                key="confirm_password"
            )

            st.write("")

            if st.button(
                "Create Account",
                type="primary",
                use_container_width=True,
                key="register_button"
            ):

                if not new_username or not new_password:

                    st.warning(
                        "Please complete all fields."
                    )

                elif new_password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                elif len(new_password) < 6:

                    st.warning(
                        "Password must contain at least 6 characters."
                    )

                else:

                    success, message = register_user(
                        new_username.strip(),
                        new_password
                    )

                    if success:

                        st.success(message)

                        st.info(
                            "Account created successfully. "
                            "You can now sign in."
                        )

                    else:

                        st.error(message)

    

    st.stop()


# ============================================================
# NAVIGATION
# ============================================================

nav_left, nav_center, nav_right = st.columns(
    [2.8, 4, 2.2]
)


# ============================================================
# BRAND
# ============================================================

with nav_left:

    st.markdown(
        """
        <div class="brand">
            🎬 Movie Recommendation System
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# NAVIGATION MENU
# ============================================================

with nav_center:

    current_page = st.radio(
        "Navigation",
        [
            "Home",
            "Discover",
            "About"
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="main_navigation"
    )

    st.session_state.page = current_page


# ============================================================
# LOGOUT
# ============================================================

with nav_right:

    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.recommendations = []
        st.session_state.selected_movie = ""
        st.session_state.page = "Home"

        st.rerun()


st.divider()


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "Home":

    st.markdown(
        '<div class="hero-label">MOVIE DISCOVERY</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">'
        'What are you watching tonight?'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">'
        'Choose a movie you already love and discover '
        'movies with similar stories, genres and themes.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    # --------------------------------------------------------
    # MOVIE SELECTION
    # --------------------------------------------------------

    movie_titles = (
        movies["title"]
        .astype(str)
        .tolist()
    )

    default_index = 0

    if (
        st.session_state.selected_movie
        and
        st.session_state.selected_movie in movie_titles
    ):

        default_index = movie_titles.index(
            st.session_state.selected_movie
        )

    selected_movie = st.selectbox(
        "🔎 Search or choose a movie",
        movie_titles,
        index=default_index,
        key="home_movie_select"
    )

    st.write("")

    # --------------------------------------------------------
    # SELECTED MOVIE
    # --------------------------------------------------------

    selected_data = movies[
        movies["title"] == selected_movie
    ]

    if not selected_data.empty:

        selected = selected_data.iloc[0]

        poster_col, details_col = st.columns(
            [1, 2.4],
            gap="large"
        )

        # ----------------------------------------------------
        # POSTER
        # ----------------------------------------------------

        with poster_col:

            show_poster(selected_movie)

        # ----------------------------------------------------
        # DETAILS
        # ----------------------------------------------------

        with details_col:

            safe_title = html.escape(
                str(selected_movie)
            )

            safe_genre = html.escape(
                str(
                    selected.get(
                        "genre",
                        "Unknown"
                    )
                )
            )

            safe_description = html.escape(
                str(
                    selected.get(
                        "description",
                        ""
                    )
                )
            )

            st.markdown(
                f"""
                <div class="movie-name">
                    {safe_title}
                </div>

                <div class="movie-genre">
                    🎭 {safe_genre}
                </div>

                <div class="movie-description">
                    {safe_description}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            if st.button(
                "✨ Find Similar Movies",
                type="primary",
                use_container_width=True,
                key="recommend_button"
            ):

                recommendations = recommend_movies(
                    selected_movie,
                    movies,
                    similarity,
                    number=5
                )

                st.session_state.recommendations = (
                    recommendations
                )

                st.session_state.selected_movie = (
                    selected_movie
                )

                st.rerun()

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    if st.session_state.recommendations:

        st.divider()

        st.markdown(
            '<div class="section-label">'
            'PERSONALIZED RECOMMENDATIONS'
            '</div>',
            unsafe_allow_html=True
        )

        st.header(
            f"Because you liked "
            f"{st.session_state.selected_movie}"
        )

        recommendations = (
            st.session_state.recommendations
        )

        columns = st.columns(
            len(recommendations),
            gap="medium"
        )

        for index, movie in enumerate(
            recommendations
        ):

            with columns[index]:

                movie_title = str(
                    movie.get(
                        "title",
                        ""
                    )
                )

                show_poster(
                    movie_title
                )

                safe_title = html.escape(
                    movie_title
                )

                safe_genre = html.escape(
                    str(
                        movie.get(
                            "genre",
                            "Unknown"
                        )
                    )
                )

                safe_description = html.escape(
                    str(
                        movie.get(
                            "description",
                            ""
                        )
                    )
                )

                score = movie.get(
                    "score",
                    0
                )

                st.markdown(
                    f"""
                    <div class="card-title">
                        {safe_title}
                    </div>

                    <div class="card-genre">
                        🎭 {safe_genre}
                    </div>

                    <div class="card-description">
                        {safe_description}
                    </div>

                    <div class="match-label">
                        MATCH
                    </div>

                    <div class="match-value">
                        {score}%
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ------------------------------------------------
                # FAVORITE
                # ------------------------------------------------

                favorite = (
                    movie_title
                    in st.session_state.favorites
                )

                if st.button(
                    "♥ Favorited"
                    if favorite
                    else "♡ Favorite",
                    key=(
                        f"favorite_{index}_"
                        f"{movie_title}"
                    ),
                    use_container_width=True
                ):

                    if favorite:

                        st.session_state.favorites.remove(
                            movie_title
                        )

                    else:

                        st.session_state.favorites.append(
                            movie_title
                        )

                    st.rerun()


# ============================================================
# DISCOVER PAGE
# ============================================================

elif st.session_state.page == "Discover":

    st.markdown(
        '<div class="hero-label">EXPLORE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="discover-title">'
        'Discover Movies'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Browse and search movies available in the system."
    )

    st.write("")

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    search = st.text_input(
        "🔎 Search movies",
        placeholder="Type a movie name..."
    )

    st.write("")

    if search:

        filtered = movies[
            movies["title"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    else:

        filtered = movies

    st.caption(
        f"Showing {len(filtered)} movies"
    )

    st.write("")

    # --------------------------------------------------------
    # DISPLAY MAXIMUM 20 MOVIES
    # --------------------------------------------------------

    display_movies = filtered.head(20)

    if display_movies.empty:

        st.warning(
            "No movies found."
        )

    else:

        columns = st.columns(
            5,
            gap="medium"
        )

        for index, (_, movie) in enumerate(
            display_movies.iterrows()
        ):

            with columns[index % 5]:

                movie_title = str(
                    movie["title"]
                )

                show_poster(
                    movie_title
                )

                safe_title = html.escape(
                    movie_title
                )

                safe_genre = html.escape(
                    str(
                        movie.get(
                            "genre",
                            "Unknown"
                        )
                    )
                )

                st.markdown(
                    f"""
                    <div class="card-title">
                        {safe_title}
                    </div>

                    <div class="card-genre">
                        🎭 {safe_genre}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "Recommend",
                    key=(
                        f"discover_{index}_"
                        f"{movie_title}"
                    ),
                    use_container_width=True
                ):

                    st.session_state.selected_movie = (
                        movie_title
                    )

                    st.session_state.recommendations = (
                        recommend_movies(
                            movie_title,
                            movies,
                            similarity,
                            number=5
                        )
                    )

                    st.session_state.page = "Home"

                    st.rerun()


# ============================================================
# ABOUT PAGE
# ============================================================

elif st.session_state.page == "About":

    st.markdown(
        '<div class="hero-label">ABOUT THE PROJECT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="discover-title">'
        'Movie Recommendation System'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.write(
        "Movie Recommendation System is a content-based "
        "machine learning application designed to help users "
        "discover movies similar to movies they already enjoy."
    )

    st.divider()

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # RECOMMENDATION ENGINE
    # --------------------------------------------------------

    with col1:

        st.subheader("🤖 Recommendation Engine")

        st.write(
            "Movie genres and descriptions are converted into "
            "numerical representations using TF-IDF. "
            "Cosine similarity is then used to identify "
            "movies with similar content."
        )

    # --------------------------------------------------------
    # TMDB
    # --------------------------------------------------------

    with col2:

        st.subheader("🎬 TMDB Integration")

        st.write(
            "TMDB provides movie posters and visual information "
            "so the recommendation interface feels more like "
            "a real movie discovery application."
        )

    st.write("")
    st.write("")

    # --------------------------------------------------------
    # TECHNOLOGY STACK
    # --------------------------------------------------------

    st.subheader("🛠️ Technology Stack")

    tech1, tech2, tech3, tech4 = st.columns(4)

    with tech1:
        st.info("🐍 Python")

    with tech2:
        st.info("⚡ Streamlit")

    with tech3:
        st.info("🤖 Machine Learning")

    with tech4:
        st.info("🎬 TMDB API")

    st.divider()

    # --------------------------------------------------------
    # MOVIE COLLECTION
    # --------------------------------------------------------

    st.subheader("📊 Movie Collection")

    st.metric(
        "Movies Available",
        len(movies)
    )


## ============================================================
# FOOTER
# ============================================================

st.divider()

st.write("🎬 Movie Recommendation System")
st.write("Discover • Explore • Recommend")