import streamlit as st
import requests
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
from io import BytesIO
import pyperclip
import textstat
from textblob import TextBlob


# Add the welcome description at the top of the main page
st.write("""
🔗 **Welcome to TextExtractor for ChatGPT!**

Need raw text from a URL to use with ChatGPT? You're in the right place. Just paste the link, and we'll fetch the text for you.

🚀 **Main Features**:
- **URL to Text**: Easily extract clean text to plug into ChatGPT.
- **PDF Support**: Not just URLs! Bring in your PDFs too.

🎁 **Bonus Insights**:
Get a quick rundown on your content with word count, mood vibes (sentiment), and readability scores.r
""")

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive', analysis.sentiment.polarity
    elif analysis.sentiment.polarity == 0:
        return 'Neutral', analysis.sentiment.polarity
    else:
        return 'Negative', analysis.sentiment.polarity

def extract_web_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return '\n'.join([p.get_text() for p in soup.find_all('p')])
    except requests.RequestException as e:
        return str(e)

def extract_pdf_content(pdf_stream):
    try:
        text = extract_text(pdf_stream)
        return text
    except Exception as e:
        return str(e)

def extract_headings(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        headings = {'H1': [], 'H2': [], 'H3': [], 'H4': [], 'H5': [], 'H6': []}
        for key in headings.keys():
            headings[key] = [tag.get_text() for tag in soup.find_all(key.lower())]
        return headings
    except requests.RequestException as e:
        return str(e)

st.sidebar.image("TextExtractor-logo.png", use_column_width=True)
st.title('	:magic_wand: Content Extractor')
option = st.sidebar.radio(
    'Choose an extractor:',
    ('URL Extractor', 'PDF Extractor')
    
)



# Add enough vertical space to push the badges to the bottom
st.sidebar.write("<br>"*15, unsafe_allow_html=True)

# Add the "Buy Me a Coffee" button code directly
st.sidebar.write(" ")
st.sidebar.markdown('<a href="https://www.buymeacoffee.com/robK"><img src="https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=robK&button_colour=FFDD00&font_colour=000000&font_family=Inter&outline_colour=000000&coffee_colour=ffffff" /></a>', unsafe_allow_html=True)

# Add a button to the left sidebar
st.sidebar.write(" ")
st.sidebar.markdown("[![Twitter](https://img.shields.io/twitter/follow/Rob_Rizk?style=social)](https://twitter.com/RobRizk2020)")

# Add a Facebook badge/button to the left sidebar
st.sidebar.write(" ")
st.sidebar.markdown("[![Facebook](https://img.shields.io/badge/Facebook-%231877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/rabihrizk/)")


url = ""
uploaded_file = None
pdf_url = ""
content = ""

if option == 'URL Extractor':
    st.subheader('Web Content Extractor')
    url = st.text_input('Enter the URL to extract content from:', '')
    if url:
        with st.spinner('Fetching and extracting content...'):
            content = extract_web_content(url)
        st.text_area('Extracted Content:', content, height=300)

elif option == 'PDF Extractor':
    st.subheader('PDF Content Extractor')
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    pdf_url = st.text_input('Or enter a PDF URL:', '')
    if uploaded_file:
        with st.spinner('Extracting content from uploaded PDF...'):
            content = extract_pdf_content(uploaded_file)
        st.text_area('Extracted Content:', content, height=300)
    elif pdf_url:
        with st.spinner('Downloading and extracting content from PDF URL...'):
            response = requests.get(pdf_url)
            pdf_stream = BytesIO(response.content)
            content = extract_pdf_content(pdf_stream)
        st.text_area('Extracted Content:', content, height=300)


if content:
    st.subheader(':bar_chart: Content Analysis')
    
    word_count = len(content.split())  # Calculate word_count here
    fk_score = textstat.flesch_reading_ease(content)  # Calculate fk_score here

    if fk_score >= 90:
        interpretation = "Very Easy"
        interpretation_color = "green"
    elif fk_score >= 80:
        interpretation = "Easy"
        interpretation_color = "green"
    elif fk_score >= 70:
        interpretation = "Fairly Easy"
        interpretation_color = "green"
    elif fk_score >= 60:
        interpretation = "Standard"
        interpretation_color = "orange"
    elif fk_score >= 50:
        interpretation = "Fairly Difficult"
        interpretation_color = "red"
    elif fk_score >= 30:
        interpretation = "Difficult"
        interpretation_color = "red"
    else:
        interpretation = "Very Confusing"
        interpretation_color = "red"

    # Sentiment Analysis
    sentiment, polarity = analyze_sentiment(content)
    if sentiment == "Positive":
        color = "green"
    elif sentiment == "Neutral":
        color = "blue"
    else:
        color = "red"
    st.markdown(f"**Sentiment Analysis**: <span style='color: {color}'>{sentiment}</span> (Polarity: {polarity:.2f})", unsafe_allow_html=True)
    
    # Using columns to organize the layout
    col1, col2 = st.columns(2)
    
    # Word Count
    with col1:
        st.markdown("**Word Count**")
        st.markdown(f"<h1 style='color: green;'>{word_count}</h1>", unsafe_allow_html=True)


    # Flesch-Kincaid readability score
    with col2:
        st.markdown("**Flesch-Kincaid Readability Score**")
        st.markdown(f"<h2 style='color: orange;'>{fk_score:.2f}</h2>", unsafe_allow_html=True)
        st.markdown(f"<span style='text-align: center; color: {interpretation_color};'>Interpretation: {interpretation}</span>", unsafe_allow_html=True)

# Add the footer section at the bottom of the main page
st.write("""
---
Got feedback or questions? I am a message away at [hello@rizkadvertising.com](mailto:hello@rizkadvertising.com).
""")

