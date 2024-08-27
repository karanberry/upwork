# Import necessary libraries
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
from datetime import datetime, timedelta
import nltk
from nltk.corpus import stopwords
import re
# Download NLTK stopwords
nltk.download('stopwords')
import hashlib
import plotly.graph_objs as go
from collections import Counter

# Download NLTK stopwords
nltk.download('stopwords')

# Load the dataset
df = pd.read_csv('clean_chatgpt_reviews.csv', parse_dates=['at'])

# Function to clean text
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower())  # Remove punctuation and convert to lowercase
    return ' '.join([word for word in text.split() if word not in set(stopwords.words('english'))])

def create_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, 
                          background_color='white', 
                          min_font_size=10).generate(text)
    
    # Convert the word cloud to an array
    word_cloud_array = wordcloud.to_array()
    
    # Create a Plotly figure
    fig = go.Figure(data=[go.Image(z=word_cloud_array)])
    
    # Update the layout to remove axes and make it look cleaner
    fig.update_layout(
        xaxis={'showgrid': False, 'showticklabels': False, 'zeroline': False},
        yaxis={'showgrid': False, 'showticklabels': False, 'zeroline': False},
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

# Streamlit app
st.title('ChatGPT Reviews Analysis')

# Create a slider for selecting the week
min_date = df['at'].min().date()
max_date = df['at'].max().date()
selected_date = st.slider('Select a date', min_value=min_date, max_value=max_date, value=min_date)

# Filter data based on selected date
selected_week = pd.Timestamp(selected_date).to_period('W')
filtered_df = df[df['at'].dt.to_period('W') == selected_week]

# Create word cloud
if not filtered_df.empty:
    text = ' '.join(filtered_df['content'].apply(clean_text))
    fig = create_wordcloud(text)
    
    st.subheader(f'Word Cloud for Week of {selected_week}')
    st.plotly_chart(fig)
else:
    st.write('No reviews for the selected week.')

# Display some statistics
st.subheader('Statistics')
st.write(f"Total reviews for the selected week: {len(filtered_df)}")
st.write(f"Average rating for the selected week: {filtered_df['score'].mean():.2f}")
