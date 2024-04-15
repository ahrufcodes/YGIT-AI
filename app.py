import os
import openai
import streamlit as st

# UI Configuration
st.set_page_config(page_title="YGIT", page_icon="💙")

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

def get_career_roadmap(career, experience_level):
    prompt_message = (
        f"Create a detailed and structured learning roadmap for{career} field at a {experience_level.lower()} level. "
        f"Include an a detailed introduction to the field, all what to know about it, what they need to know at this level, links to courses, book recommendations,"
        f"Include YouTube videos/playlists, and article recommendations. Provide hands-on project ideas and GitHub repositories where applicable. "
        f"Also, include a list of communities, forums, and social media accounts to follow for networking and learning. "
        f"Include a list of job boards, websites, and platforms to find job opportunities and internships. "
        f"Lastly, provide a list of tools, software, and technologies to learn and master for this career."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant skilled in providing comprehensive career guidance. You offer detailed insights into various tech careers, including educational resources, practical tips, and professional development strategies"},
                {"role": "user", "content": prompt_message}
            ],
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        if response.choices:
            return response.choices[0].message['content']
        else:
            return "No response was generated."
    except Exception as e:
            return f"Error processing your request: {str(e)}"




# Button to generate the roadmap + loading state
if st.button('Generate Roadmap'):
    if career:
        with st.spinner('cooking your roadmap, wait a minute.'):
            roadmap = get_career_roadmap(career, experience_level)
            st.success('Yay here is your roadmap')
        st.markdown("### Here is  Your Personalized Tech Career Roadmap")
        st.markdown(roadmap, unsafe_allow_html=True)
    else:
        st.warning('Please enter a tech career to generate your roadmap.')


#Footer and all
footer="""<style>
a:link , a:visited{
color: #B7B7B7;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: #102755;
background-color: transparent;
text-decoration: underline;
}

.footer {
position:fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #919FB6;
color: #fffff;
text-align: center;
}
</style>
<div class="footer">
<p> Developed with ❤️ by <a href="https://github.com/ahrufcodes" target="_blank">ahruf</a> </p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)