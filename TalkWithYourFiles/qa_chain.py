from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from parameter_controller import ParameterController

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
    ## by default it uses 'text-davinci-003' model from OpenAI, for simpler tasks with reduced costs 'gpt-3.5-turbo' can be used.
    def __init__(self, param_controller):
        """Initialize the QAChainRunner with a specific model.
        To use we need one instance of this class & the use of the setup method.

        Parameters:
        model_name (str): The name of the model to use.

        """
        self.param_controller = param_controller


        self.model_name = None
        self.top_related_chunks = None
        self.llm = None

    def setup(self, api_key):
        # authorizing with openai api key
        self.api_key = api_key

        # to be used in the get_relative_chunks function
        self.top_related_chunks = self.param_controller.get_parameter('top_related_chunks')['value']
        
        # to be used when initialising the model.
        self.model_name = self.param_controller.get_parameter('model_name')['value']
        self.requested_max_model_tokens = self.param_controller.get_parameter('requested_max_model_tokens')['value']
    
        # initialise the model
        self.llm = OpenAI(
                        model_name=self.model_name,
                        max_tokens=self.requested_max_model_tokens,
                        OPENAI_API_KEY=api_key
                        )

        # to be used with chain specific params
        self.displayed_max_response_tokens = self.param_controller.get_parameter('displayed_max_response_tokens')['value']



    def get_relative_chunks(self, knowledge_base, user_question):
        """Find the chunks in the knowledge base that are most relevant to the user's question.

        Parameters:
        knowledge_base: The vector store that contains the knowledge base.
        user_question (str): The question from the user.

        Returns:
        List[str]: The most relevant chunks.

        """
        try:
            return knowledge_base.similarity_search(
                                                    user_question, 
                                                    k=self.top_related_chunks
                                                    )
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
            chain = load_qa_chain(
                                self.llm, 
                                chain_type="stuff"
                                ) 
            with get_openai_callback() as callback:
                print(self.llm)
                response = chain.run(
                                    input_documents=docs, 
                                    question=user_question,
                                    max_tokens=self.displayed_max_response_tokens
                                    )

                print(callback)
            return response
        except Exception as e:
            print(f"Error running QA chain: {e}")
            return ""
