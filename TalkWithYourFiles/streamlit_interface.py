import streamlit as st
from flow_coordinator import run

"""
This file follows the dependency inversion principle, and separates UI from backend functionalities:
Streamlit framework is used to render the GUI and manage file uploads.
To use other approaches or frameworks: 
1) Make sure to set up a GUI that allows users to upload files & enter text input for their questions.
2) Import the run method from the flow_coordinator.py
3) Get the response by running the run(files, user_question) method with the appropriate arguments. 

"""


def main():
    """Main function to run the Streamlit interface and execute the run function from file_processor."""

    st.set_page_config(page_title="Talk With Your Files")  # can add parameters to style the page
    st.header("Talk With Your Files")

    files = st.file_uploader("Upload files", type=["pdf", "docx", "txt","csv"], accept_multiple_files=True)
    user_question = st.text_input("Please ask me about your uploaded files and I shall help you: ")

    if user_question and files:
        response = run(files, user_question)
        st.write(response)

if __name__ == '__main__':
    main()
