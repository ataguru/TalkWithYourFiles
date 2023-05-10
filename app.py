from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback



def main():
    load_dotenv() # allows the environment variables to be used e.g print(os.getenv("OPENAI_API_KEY"))
    st.set_page_config(page_title="Ask me about your PDF") # can add parameteres to style the page
    st.header("Ask me about your PDF ..")

    # upload the file
    pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

    # extract the text
    if pdf is not None:
        pdf_reader = PdfReader(pdf) 
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator= "\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len #defining a function to be used for measuring
        )

        chunks = text_splitter.split_text(text)

        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks,embeddings)

        # show user input
        user_question = st.text_input("Ask me a question about your PDF:")
        if user_question:
            # relative chunks
            docs = knowledge_base.similarity_search(user_question, k=5) # add k parameter to limit the number of results
            
            llm = OpenAI()

            chain = load_qa_chain(llm, chain_type="stuff")

            # inside of this run whatever we want to track the price of
            ## currently this langchain function only works with open AI
            with get_openai_callback() as callback:
                response = chain.run(input_documents=docs, question=user_question)
                print(callback)

            st.write(response)



if __name__ == '__main__':
    main()

