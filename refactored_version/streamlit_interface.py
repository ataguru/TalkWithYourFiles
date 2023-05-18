import streamlit as st
from file_processor import run

def main():
    """Main function to run the Streamlit interface and execute the run function from file_processor."""

    st.set_page_config(page_title="Ask me about your PDF")  # can add parameters to style the page
    st.header("Ask me about your PDF ..")

    files = st.file_uploader("Upload files", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    user_question = st.text_input("Ask me a question about your PDF:")

    if user_question and files:
        response = run(files, user_question)
        st.write(response)

if __name__ == '__main__':
    main()
