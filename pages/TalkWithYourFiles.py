from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback




def upload_pdf():
    # upload the file
    pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    return pdf


## maybe introduce this later
# def upload_file():
#     # upload the file, now supporting pdf, docx and txt files
#     file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt"])
#     return file



def extract_text_from_pdf(pdf):
    # extract the text
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx):
    # code for extracting text from a Word document
    print("Code to extract text from a Word document goes here")


def get_raw_text():
    # get raw text input from the user
    text = st.text_area("Or enter your text here:")
    return text



def split_text_into_chunks(text):
    # split into chunks
    text_splitter = CharacterTextSplitter(
        separator= "\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def create_embeddings(chunks):
    # create embeddings
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks,embeddings)
    return knowledge_base

def get_user_question():
    # show user input
    user_question = st.text_input("Ask me a question about your PDF:")
    return user_question

def get_relative_chunks(knowledge_base, user_question):
    # relative chunks
    docs = knowledge_base.similarity_search(user_question, k=5) # add k parameter to limit the number of results
    return docs

def run_chain(llm, docs, user_question):
    chain = load_qa_chain(llm, chain_type="stuff")
    # inside of this run whatever we want to track the price of
    ## currently this langchain function only works with open AI
    with get_openai_callback() as callback:
        response = chain.run(input_documents=docs, question=user_question)
        print(callback)
    return response



def main():
    load_dotenv() # allows the environment variables to be used e.g print(os.getenv("OPENAI_API_KEY"))
    st.set_page_config(page_title="Ask me about your PDF") # can add parameters to style the page
    st.header("Ask me about your PDF ..")


    ## decide to remove or not.
    # # maybe show after a click of a button?
    # # copy paste a text to question
    # user_text = st.text_area("Enter your text here:")



    # get a pdf upload
    pdf = upload_pdf()


    user_question = get_user_question()

    if user_question:
        if pdf is not None:
            text = extract_text_from_pdf(pdf)

            chunks = split_text_into_chunks(text)
            knowledge_base = create_embeddings(chunks)
            docs = get_relative_chunks(knowledge_base, user_question)
            llm = OpenAI()
            response = run_chain(llm, docs, user_question)
            st.write(response)

if __name__ == '__main__':
    main()
