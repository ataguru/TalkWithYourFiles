import logging
from dotenv import load_dotenv
from file_handlers import FileHandlerFactory
from text_processor import DefaultTextProcessor
from qa_chain import QAChainRunner

load_dotenv()
logging.basicConfig(level=logging.INFO)

factory = FileHandlerFactory()
processor = DefaultTextProcessor() #the name is not confusing due to having multiple processors. Turn it to text_processor and update the rest.
runner = QAChainRunner()

def run(files, user_question):
    """Main function to process uploaded files and user's question, and run QA chain runner.

    Args:
        files: List of uploaded files.
        user_question: User's question input.

    Returns:
        str: The response from the QA chain runner.
    """

    if files and len(files) > 3:
        logging.warning("Please upload a maximum of 3 files")
        return "Please upload a maximum of 3 files"

    if user_question and files:
        combined_text = ""
        for file in files:
            if file is not None:
                handler = factory.get_file_handler(file.type)
                text = handler.read_file(file)
                if not text:
                    logging.error(f"No text could be extracted from {file.name}. Please ensure the file is not encrypted or corrupted.")
                    return f"No text could be extracted from {file.name}. Please ensure the file is not encrypted or corrupted."
                else:
                    combined_text += text

        if not combined_text:
            logging.warning("No text could be extracted from the provided files. Please try again with different files.")
            return "No text could be extracted from the provided files. Please try again with different files."

        chunks = processor.split_text(combined_text)
        if not chunks:
            logging.warning("Couldn't split the text into chunks. Please try again with different text.")
            return "Couldn't split the text into chunks. Please try again with different text."

        knowledge_base = processor.create_embeddings(chunks)
        if not knowledge_base:
            logging.warning("Couldn't create embeddings from the text. Please try again.")
            return "Couldn't create embeddings from the text. Please try again."

        docs = runner.get_relative_chunks(knowledge_base, user_question)
        if not docs:
            logging.warning("Couldn't find any relevant chunks for your question. Please try asking a different question.")
            return "Couldn't find any relevant chunks for your question. Please try asking a different question."

        return runner.run_chain(docs, user_question)
