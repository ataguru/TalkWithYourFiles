from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

class QAChainRunner:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.llm = OpenAI(model_name=model_name)

    def get_relative_chunks(self, knowledge_base, user_question):
        return knowledge_base.similarity_search(user_question, k=1)

    def run_chain(self, docs, user_question):
        chain = load_qa_chain(self.llm, chain_type="stuff")
        with get_openai_callback() as callback:
            response = chain.run(input_documents=docs, question=user_question)
            print(callback)
        return response
