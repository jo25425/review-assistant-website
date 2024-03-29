import json
import os
from random import choice
import streamlit as st
from streamlit import session_state
import requests


API_URL = os.environ.get('API_URL')
# API_URL = 'http://127.0.0.1:8000/' # Uncomment to use local API

ERROR_MESSAGE_TEMPLATE = """
Could not get {requested}

{error}
"""

EXAMPLE_PRODUCTS = [
    "Nike Initiator Shoes in White for Men",
    "iPhone 15",
    "Hydro flask water bottle",
    "Maybelline Instant Age Rewind Eraser Dark Circles Treatment Concealer"
]

st.set_page_config(page_title="Review Writing Assistant")

if 'product' not in session_state:
    session_state.product = choice(EXAMPLE_PRODUCTS)
if 'criteria_clicked' not in session_state:
    session_state.criteria_clicked = False
if 'reviews_clicked' not in session_state:
    session_state.reviews_clicked = False


def click_criteria_button():
    session_state.product = product
    session_state.criteria_clicked = True
    session_state.reviews_clicked = False


def click_reviews_button():
    session_state.reviews_clicked = True


@st.cache_data()
def get_criteria(current_product):
    # Dummy data
    if API_URL is None:
        return ["Coverage", "Longevity", "Application", "Shade range",
                "Packaging", "Skincare benefits"]

    res = requests.get(API_URL + 'criteria', params=dict(product=current_product))
    res.raise_for_status()
    criteria = res.json()
    return criteria


@st.cache_data()
def get_reviews(current_product, current_rated_criteria):
    if API_URL is None:
        return [
            "The product arrived in excellent condition, exactly as described "
            "on their website. I'm thrilled with the quality and will definitely "
            "buy it again in the future. Highly recommended!",

            "The product quality is consistently outstanding, exceeding my expectations every time.",

            "Really good quality, lovely packaging & smells amazing. Affordable price."
        ]
    res = requests.post(
        API_URL + 'reviews',
        params=dict(product=current_product, rated_criteria=json.dumps(current_rated_criteria))
    )
    res.raise_for_status()
    reviews = res.json()
    return reviews


def rate_criteria(criteria: list[str]):

    with st.form('criteria_form'):
        '''How would you rate the following?'''
        ''''''
        rated_criteria = {}
        for i, criterium in enumerate(criteria):
            with st.container():  # Creates a row
                col1, col2 = st.columns([2,3])
                # Label
                col1.markdown(criterium.capitalize())
                # Slider for the rating
                rated_criteria[criterium] = col2.slider(
                    criterium.title(),
                    min_value=1,
                    max_value=5,
                    value=3,
                    key=f'criterium_{i}',
                    label_visibility='collapsed'
                )
        session_state.rated_criteria = rated_criteria
        st.form_submit_button("Go!", on_click=click_reviews_button)


def show_reviews(reviews: list[str]):
    '''Here are some reviews you could use.'''
    for i, review in enumerate(reviews):
        st.text_area(f"##### Review #{i+1}", review, key=f'review_{i}',
                     height=int(len(review) / 2.5))  # Just from eyeballing


'''# Review Writing Assistant ⭐️📝'''

# Section from product input
with st.form('product_form'):
    product = st.text_area(label="Which product do you want to review?",
                           value=session_state.product,
                           max_chars=100)
    session_state.product = product
    go_criteria = st.form_submit_button("Go!", on_click=click_criteria_button)


# Section for rating criteria
if session_state.criteria_clicked:
    try:
        criteria = get_criteria(session_state.product)
        rate_criteria(criteria)

    except requests.RequestException as e:
        message = ERROR_MESSAGE_TEMPLATE.format(requested='criteria', error=e)
        st.error(message, icon='❌')

# Section for showing reviews
if session_state.reviews_clicked:
    try:
        reviews = get_reviews(session_state.product, session_state.rated_criteria)
        show_reviews(reviews)

    except Exception as e:
        message = ERROR_MESSAGE_TEMPLATE.format(requested='reviews', error=e)
        st.error(message, icon='❌')
