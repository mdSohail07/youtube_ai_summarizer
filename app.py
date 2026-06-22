import streamlit as st
from dotenv import load_dotenv

load_dotenv()  ## load all the environment variables

import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """
You are YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:
"""

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        # Extract video id
        video_id = youtube_video_url.split("v=")[1].split("&")[0]

        # New API syntax
        api = YouTubeTranscriptApi()
        transcript_data = api.fetch(video_id)

        transcript = ""
        for item in transcript_data:
            transcript += " " + item.text

        return transcript

    except Exception as e:
        st.error(f"Error: {e}")
        return None


## getting the summary based on Prompt from Google Gemini
def generate_gemini_content(transcript_text, prompt):

    # Replace gemini-pro with latest model
    model = genai.GenerativeModel("gemini-2.0-flash")

    response = model.generate_content(prompt + transcript_text)

    return response.text


st.title("YouTube Transcript to Detailed Notes Converter")

youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("v=")[1].split("&")[0]

    st.image(
        f"https://img.youtube.com/vi/{video_id}/0.jpg",
        width="stretch"
    )

if st.button("Get Detailed Notes"):

    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)

        st.markdown("## Detailed Notes:")

        st.write(summary)