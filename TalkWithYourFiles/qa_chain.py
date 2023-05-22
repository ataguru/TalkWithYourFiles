from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

"""
In this file QAChainRunner class is implemented, which is responsible for running the Question Answering (QA) chain
on provided documents and questions.

The class utilizes the Langchain library for the underlying question answering capabilities.

Usage:
    1. Create an instance of QAChainRunner.
    1.1 Optionally, specify the model name to use from OpenAI.
    1.2 To use non-OpenAI models modify the self.llm instance variable.
    2. Use the 'get_relative_chunks' method to find the most relevant chunks in the knowledge base for a given question.
    3. Use the 'run_chain' method to execute the QA chain on the provided documents and question.

Design Pattern:
    This class follows the Chain of Responsibility design pattern, where each step in the QA chain acts as a handler
    and can process the question or pass it to the next handler.
    """

class QAChainRunner:
    def __init__(self, model_name="gpt-3.5-turbo"):
        """Initialize the QAChainRunner with a specific model.

        Parameters:
        model_name (str): The name of the model to use.

        """
        self.llm = OpenAI(model_name=model_name)

    def get_relative_chunks(self, knowledge_base, user_question):
        """Find the chunks in the knowledge base that are most relevant to the user's question.

        Parameters:
        knowledge_base: The vector store that contains the knowledge base.
        user_question (str): The question from the user.

        Returns:
        List[str]: The most relevant chunks.

        """
        try:
            amount_of_top_chunks_to_return = 3
            return knowledge_base.similarity_search(user_question, k=amount_of_top_chunks_to_return)
        except Exception as e:
            print(f"Error finding relative chunks: {e}")
            return []

    def run_chain(self, docs, user_question):
        """Run the QA chain on the provided documents and question.

        Parameters:
        docs (List[str]): The documents to use in the QA chain.
        user_question (str): The question to answer.

        Returns:
        str: The response from the QA chain.

        """
        try:
            chain = load_qa_chain(self.llm, chain_type="stuff")
            with get_openai_callback() as callback:
                response = chain.run(input_documents=docs, question=user_question)
                print(callback)
            return response
        except Exception as e:
            print(f"Error running QA chain: {e}")
            return ""
