# review-assistant-website
Frontend for the review writing assistant (final project from Le Wagon Machine Learning Bootcamp)

### Application description

1. _Input 1_: The user provides a title or description for the product they want to review.
2. _Inference 1_: Given this product description, our application generates a list of criteria to rate.
3. _Input 2_: The user provides a rating for whichever criteria they'd like.
4. _Inference 2_: Given the rated criteria, our application generates a few possible reviews.

<img width="1001" alt="Web interface preview with an input for the product name and some sliders to provide ratings" src="https://github.com/jo25425/review-assistant-website/assets/1435192/068102af-fe40-472b-8417-6ad28cf9983a">

### Deployment

#### Locally

The requirements can be automatically installed with:
`make install_requirements`

The app can then be run locally with:
`make streamlit`

ℹ️ When running locally, the API this frontend points to should be adjusted directly in the code.

#### On Streamlit Cloud

This application is registered with streamlit.io. It automatically updates according to the main branch.

It can be accessed at the following address: http://review-writing-assistant.streamlit.app 🚀

ℹ️ If the app isn't used by anyone for a while, it might need to be reactivated first.
