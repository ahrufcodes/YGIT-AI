import os
import openai
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pdf_generator import generate_pdf_roadmap
#from mu import generate_pdf_roadmap


# Load environment variables from the .env file
load_dotenv()

# Initialize the OpenAI client using the API key from the environment variable
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# UI Configuration
st.set_page_config(page_title="YGIT", page_icon="💙")



# Custom CSS for styling
st.markdown("""
<style>
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
    }
    .brand {
        font-size: 1.5rem;
        font-weight: bold;
        color: #3B6AC8;
    }
    .nav-links {
        display: flex;
        gap: 1rem;
    }
    .nav-link {
        color: #333;
        text-decoration: none;
        font-weight: 500;
    }
    .nav-link:hover {
        color: #3B6AC8;
    }
    .sidebar-link {
        display: block;
        padding: 0.5rem 0;
        color: #333;
        text-decoration: none;
    }
    .sidebar-link:hover {
        color: #3B6AC8;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <div class="brand">YGIT</div>
    <div class="nav-links">
        <a href="#" class="nav-link">Home</a>
        <a href="#" class="nav-link">About</a>
        <a href="#" class="nav-link">Roadmap</a>
        <a href="#" class="nav-link">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)


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


# Display an Image Banner
st.image('img/banner.png', use_column_width=True)
# App Main Content
st.header('Your Guide into Tech: Career Roadmap')


# User Inputs
name = st.text_input('Your Name Please')
career = st.text_input('Which tech career would you like to pursue or learn more about?')
experience_level = st.selectbox(
    'Select your current experience level:',
    ('Beginner', 'Intermediate', 'Advanced', 'Expert')
)

def get_career_roadmap(career, experience_level, name):
    prompt_message = (
        f"Create a detailed and structured learning roadmap for{career} field at a {experience_level.lower()} level. "
        f"Include an a detailed introduction to the field, all what to know about it, what they need to know at this level, links to courses, book recommendations,"
        f"Include YouTube videos/playlists, and article recommendations. Provide hands-on project ideas and GitHub repositories where applicable. "
        f"Also, include a list of communities, forums, and social media accounts to follow for networking and learning. "
        f"Include a list of job boards, websites, and platforms to find job opportunities and internships. "
        f"Lastly, provide a list of tools, software, and technologies to learn and master for this career."
        f"Personalize this roadmap for {name}." 
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant skilled in providing comprehensive career guidance. You offer detailed insights into various tech careers, including educational resources, practical tips, and professional development strategies"},
                {"role": "user", "content": prompt_message}
            ],
            temperature=0.5,
            max_tokens=2024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        if response.choices:
            return response.choices[0].message.content
        else:
            return "No response was generated."
    except Exception as e:
            return f"Error processing your request: {str(e)}"



if st.button('Generate Roadmap'):
    if career and experience_level and name:
        with st.spinner(f' {name} we are cooking 🍳 your roadmap  please wait a minute...'):
            roadmap = get_career_roadmap(career, experience_level, name)
            st.success(f'Yay! here is your roadmap, happy learning 🤍')
        st.markdown(f"### Here is Your Personalized Tech Career Roadmap {name}")
        st.markdown(roadmap, unsafe_allow_html=True)

        # Generate PDF
        pdf_filename = generate_pdf_roadmap(career, experience_level, roadmap)
        
        # Offer PDF for download
        with open(pdf_filename, "rb") as pdf_file:
            PDFbyte = pdf_file.read()
        
        st.download_button(label="Download PDF Roadmap",
                           data=PDFbyte,
                           file_name=pdf_filename,
                           mime='application/octet-stream')




footer = """
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f8f9fa;
        color: #6c757d;
        text-align: center;
        padding: 10px 0;
        font-family: 'Roboto', sans-serif;
        font-size: 10px;
        border-top: 1px solid #dee2e6;
        z-index: 100;
        transition: background-color 0.3s ease;
    }
    .footer:hover {
        background-color: #e9ecef;
    }
    .footer p {
        margin: 0;
        padding: 0;
    }
    .footer a {
        color: #007bff;
        text-decoration: none;
        transition: color 0.3s ease, transform 0.3s ease;
        display: inline-block;
    }
    .footer a:hover {
        color: #0056b3;
        transform: translateY(-2px);
    }
    .footer-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    .footer-left, .footer-right {
        display: flex;
        align-items: center;
    }
    .footer-right a {
        margin-left: 20px;
    }
    .github-icon {
        width: 20px;
        height: 20px;
        margin-right: 5px;
        vertical-align: middle;
        transition: transform 0.3s ease;
    }
    .footer-right a:hover .github-icon {
        transform: rotate(360deg);
    }
</style>

<div class="footer">
    <div class="footer-content">
        <div class="footer-left">
            <p>© 2024 YGIT </p>
        </div>
        <div class="footer-right">
            <p>Developed with <span class="heart">❤️</span> by 
                <a href="https://github.com/ahrufcodes" target="_blank">
                    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" class="github-icon" alt="GitHub">
                    ahruf
                </a>
            </p>
        </div>
    </div>
</div>

<script>
    const heart = document.querySelector('.heart');
    heart.addEventListener('mouseover', () => {
        heart.style.fontSize = '16px';
        heart.style.transition = 'font-size 0.3s ease';
    });
    heart.addEventListener('mouseout', () => {
        heart.style.fontSize = '10px';
    });
</script>
"""

st.markdown(footer, unsafe_allow_html=True)