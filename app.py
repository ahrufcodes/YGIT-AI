import os
import openai
import streamlit as st

# UI Configuration
st.set_page_config(page_title="YGIT", page_icon="img/Mark.svg")

# Google Font URL and CSS Injection for Styling
font_url = "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
css_code = f"""
<style>
@import url('{font_url}');
body, .stButton > button, .stTextInput > input, .stSelectbox > select, .css-10trblm {{
    font-family: 'Roboto', sans-serif;
}}
h1, h2, h3 {{
    color: #3B6AC8; /* Unified color styling for titles and headers */
}}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# Connect to OpenAI GPT-3
openai.api_key = os.getenv("OPENAI_API_KEY")

# Display an Image Banner
st.image('img/banner.png', use_column_width=True)

# App Main Content
st.header('Your Guide into Tech: Career Roadmap')

# User Inputs
career = st.text_input('Which tech career would you like to pursue or learn more about?')
experience_level = st.selectbox(
    'Select your current experience level:',
    ('Beginner', 'Intermediate', 'Advanced', 'Expert')
)

if st.button('Generate Roadmap'):
    if career:
        # Detailed prompt for the OpenAI model
        prompt_message = (
            f"Create a detailed and structured learning roadmap for someone aspiring to enter the {career} field at a {experience_level.lower()} level. "
            f"Include an introduction to the field, what they need to know at this level, links to courses, book recommendations, "
            f"YouTube videos/playlists, and article recommendations. Provide hands-on project ideas and GitHub repositories where applicable."
            f"Also, include a list of communities, forums, and social media accounts to follow for networking and learning."
            f"Include  "
        )

        # Fetching the completion from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an assistant that helps create detailed career roadmaps."},
                {"role": "user", "content": f"I'm interested in learning more about a career in {career} at a {experience_level} level. Can you generate a comprehensive resource list and a digital roadmap?"}
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Handling the response
        if response.choices:
            last_message = response.choices[0].message['content']
            formatted_output = "### Your Personalized Tech Career Roadmap\n" + last_message.replace("\n", "\n\n")
            st.markdown(formatted_output, unsafe_allow_html=True)
        else:
            st.error("Sorry, an error occurred while generating your roadmap.")
    else:
        st.warning('Please enter a tech career to generate your roadmap.')