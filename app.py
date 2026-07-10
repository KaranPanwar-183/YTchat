import streamlit as st
from YT_Processor.get_YT_transcript import process_youtube_transcript
from text_processor.loader import load_chunks
from text_processor.indexing import index_chunks
from usingLLM.augmented_generation import ask_question


st.set_page_config(
    page_title="video Chatbot",
    page_icon = "🤖",
    layout = "wide",
)

# ---------------- Session State ---------------- #

if "video_ready" not in st.session_state:
    st.session_state.video_ready = False

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Video Chatbot")
st.write("paste a youtube video link and ask questions about the video content")

video_url = st.text_input("Enter YouTube video URL")

if st.button("Process Video"):
    if  not video_url:
        st.warning("Please enter a YouTube video URL.")
    else:
        
        st.success("Video processing started. Please wait...")

        with st.spinner("Processing video..."):
            transcript_path = process_youtube_transcript(video_url)

        with st.spinner("hang on......."):
            chunks = load_chunks(transcript_path)
            index_chunks(chunks)
        
        st.session_state.messages = []
        st.session_state.video_ready = True
        st.success("Video processing completed! You can now ask questions about the video content.")



if st.session_state.video_ready:

    st.divider()

    st.subheader("Chat")

    # Show previous messages

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask something about the video..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("Thinking..."):
            answer = ask_question(question)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)
        
        





