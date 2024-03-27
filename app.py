import os
import streamlit as st
from streamlit import session_state
import requests

API_URL = os.environ.get('API_URL')  # Set to 'http://127.0.0.1:8000/' in .env to use local API
RATINGS_EXPLAINED = ["Very bad", "Bad", "Acceptable", "Good", "Excellent"]

if 'criteria_clicked' not in session_state:
    session_state.criteria_clicked = False
if 'reviews_clicked' not in session_state:
    session_state.reviews_clicked = False


def click_criteria_button():
    session_state.criteria_clicked = True
    session_state.reviews_clicked = False


def click_reviews_button():
    session_state.reviews_clicked = True


@st.cache_data()
def get_criteria():
    # Dummy data
    if API_URL is None:
        return ["Coverage", "Longevity", "Application", "Shade range",
                "Packaging", "Skincare benefits"]

    try:
        res = requests.get(API_URL + 'criteria', params=dict(product=product))
        if res.status_code == 200:
            criteria = res.json()
            return criteria
    except:
        return


@st.cache_data()
def get_reviews():
    if API_URL is None:
        return [
            "The product arrived in excellent condition, exactly as described "
            "on their website. I'm thrilled with the quality and will definitely "
            "buy it again in the future. Highly recommended!",

            "The product quality is consistently outstanding, exceeding my expectations every time.",

            "Really good quality, lovely packaging & smells amazing. Affordable price."
        ]
    try:
        res = requests.get(
            API_URL + 'reviews',
            params=dict(product=product, rated_criteria=session_state.rated_criteria)
        )
        if res.status_code == 200:
            reviews = res.json()
            return reviews
    except:
        return


def rate_criteria(criteria: list[str]):

    '''How would you rate the following?'''
    rated_criteria = {}
    for i, criterium in enumerate(criteria):
        with st.container():  # Creates a row
            col1, col2 = st.columns([1,3])
            # Label
            col1.text(criterium.title())
            # Slider for the rating
            rated_criteria[criterium] = col2.slider(
                criterium.title(),
                min_value=1,
                max_value=len(RATINGS_EXPLAINED),
                # captions=RATINGS_EXPLAINED if i == 0 else None,
                value=3,
                key=f'criterium_{i}',
                label_visibility='collapsed'
            )
    session_state.rated_criteria = rated_criteria
    st.button("Go!", key='go_reviews', on_click=click_reviews_button)


def show_reviews(reviews: list[str]):
    '''Here are some reviews you could use.'''
    for i, review in enumerate(reviews):
        st.text_area(f"Review #{i+1}", review, key=f'review_{i}')


'''# Review Writing Assistant ⭐️📝'''

product = st.text_area(label="Which product do you want to review?",
                       value="Maybelline Instant Age Rewind Eraser Dark Circles Treatment Concealer",
                       max_chars=100)

go_criteria = st.button("Go!", key='go_criteria', on_click=click_criteria_button)

if session_state.criteria_clicked:
    session_state.show_criteria = True
    criteria = get_criteria()
    if criteria:
        rate_criteria(criteria)
    else:
        st.error("Could not get criteria ❌")

if session_state.reviews_clicked:
    reviews = get_reviews()
    if reviews:
        show_reviews(reviews)
    else:
        st.error("Could not get reviews ❌")
