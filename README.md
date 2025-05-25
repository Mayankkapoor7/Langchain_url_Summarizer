# Langchain_url_Summarizer

 LangChain-Based Summarization App
This application leverages LangChain, Groq LLMs, and Streamlit to generate concise and coherent summaries from both YouTube videos and webpage content. It is designed to streamline content consumption by distilling lengthy material into an easily digestible format.

Project Overview
The app provides users with a simple interface to input a YouTube or website URL, extract relevant text or transcript data, and produce a structured summary using large language models hosted on Groq’s inference platform. It’s ideal for researchers, students, professionals, and anyone seeking to understand content faster without manually reading or watching everything in full.

Key Features
Summarization from YouTube
Automatically extracts transcripts from YouTube videos using youtube-transcript-api.

Summarization from Web URLs
Extracts raw text content from websites using UnstructuredURLLoader.

Powered by Groq LLMs
Utilizes LLaMA3-70B via Groq’s ultra-fast inference to generate high-quality summaries.

Prompt-Driven Summary Generation
Uses custom prompts to generate ~300-word summaries tailored to the extracted content.

Secure API Input
API keys are handled securely using password fields in the Streamlit sidebar.

