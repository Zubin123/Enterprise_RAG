import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="Enterprise SEC RAG",
    layout="wide"
)

st.title("Enterprise SEC Filing Intelligence Engine")
st.markdown("Ask natural language questions on Apple & Microsoft SEC 10-K filings")

# Input box
question = st.text_area(
    "Enter your question",
    placeholder="e.g. What are the main risk factors for Apple in 2023?",
    height=120
)

if st.button("Ask Question"):
    if not question.strip():
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            response = requests.post(
                API_URL,
                json={"question": question}
            )

            if response.status_code == 200:
                data = response.json()

                st.subheader("Answer")
                st.write(data["answer"])

            else:
                st.error("Backend error. Make sure FastAPI is running.")
