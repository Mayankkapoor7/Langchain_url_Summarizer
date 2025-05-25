import streamlit as st
import validators
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader

# Function to extract transcript from a YouTube URL
def extract_transcript_from_youtube(url):
    query = urlparse(url).query
    video_id = parse_qs(query).get("v", [None])[0]
    if not video_id:
        return []
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry["text"] for entry in transcript])
        return [Document(page_content=full_text)]
    except Exception as e:
        st.error(f"Transcript could not be retrieved: {str(e)}")
        return []

# Streamlit App Configuration
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize any YouTube or Web URL")

# Sidebar Inputs
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")
    generic_url = st.text_input("Enter YouTube or Website URL")

# Prompt Template
prompt_template = """
Provide a summary of the following content in 300 words:
Content: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# Main Button Action
if st.button("Summarize the Content from YT or Website"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide both the API key and the URL.")
    elif not validators.url(generic_url):
        st.error("Invalid URL. Please enter a valid YouTube or website URL.")
    else:
        try:
            with st.spinner("Fetching and summarizing content..."):
                # Load content
                if "youtube.com" in generic_url:
                    docs = extract_transcript_from_youtube(generic_url)
                    if not docs:
                        st.stop()
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={"User-Agent": "Mozilla/5.0"}
                    )
                    docs = loader.load()

                # Initialize LLM
                llm = ChatGroq(model="llama3-70b-8192", groq_api_key=groq_api_key)

                # Run summarization
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                st.success("Summary generated successfully!")
                st.write(output_summary)

        except Exception as e:
            st.exception(e)
