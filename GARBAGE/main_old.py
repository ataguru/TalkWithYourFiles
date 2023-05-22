from dotenv import load_dotenv
import streamlit as st
from file_handlers import FileHandlerFactory
from text_processor import DefaultTextProcessor
from qa_chain import QAChainRunner

load_dotenv()  # load environment variables

st.set_page_config(page_title="Ask me about your PDF")  # can add parameters to style the page
st.header("Ask me about your PDF ..")

# FileHandlerFactory and DefaultTextProcessor instances
factory = FileHandlerFactory()
processor = DefaultTextProcessor()
runner = QAChainRunner()  # OpenAI instance is created here

def upload_files():
    files = st.file_uploader("Upload files", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    return files

def get_user_question():
    user_question = st.text_input("Ask me a question about your PDF:")
    return user_question

def main():

    files = upload_files()

    if len(files) > 3:
        st.write("Please upload a maximum of 3 files")
        return

    user_question = get_user_question()

    if user_question:
        combined_text = ""
        for file in files:
            if file is not None:
                handler = factory.get_file_handler(file.type)
                text = handler.read_file(file)
                if not text:
                    st.write(f"No text could be extracted from {file.name}. Please ensure the file is not encrypted or corrupted.")
                else:
                    combined_text += text

        if not combined_text:
            st.write("No text could be extracted from the provided files. Please try again with different files.")
            return


        chunks = processor.split_text(combined_text)
        if not chunks:
            st.write("Couldn't split the text into chunks. Please try again with different text.")
            return

        knowledge_base = processor.create_embeddings(chunks)
        if not knowledge_base:
            st.write("Couldn't create embeddings from the text. Please try again.")
            return


        docs = runner.get_relative_chunks(knowledge_base, user_question)
        if not docs:
            st.write("Couldn't find any relevant chunks for your question. Please try asking a different question.")
            return

        
        response = runner.run_chain(docs, user_question)
        st.write(response)

if __name__ == '__main__':
    main()
