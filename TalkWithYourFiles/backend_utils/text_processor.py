from abc import ABC, abstractmethod
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


"""
In this file Strategy Design Pattern is used to make this functionalities more flexible & maintainable.
Currently there's only one text processor subclass which is called DefaultTextProcessor.

If you met the need to extend this further by adding a new text processor subclass:
1) Create a new subclass of TextProcessor in this module.
2) Implement the split_text method: Define the logic to split the text into chunks according to the desired strategy.
3) Implement the create_embeddings method: Define how to create embeddings or other representations from the text chunks.
4) Optionally, implement any additional methods specific to your text processing strategy. 

Feel free to refer to the existing DefaultTextProcessor implementation for guidance on how to structure your new text processor subclass.

"""


class TextProcessor(ABC):
    """Abstract base class for text processors."""

    @abstractmethod
    def split_text(self, text):
        """Split the text into chunks.

        Parameters:
        text (str): The text to split.

        Returns:
        list: The text chunks.

        """
        pass

    @abstractmethod
    def create_embeddings(self, chunks):
        """Create embeddings from the text chunks.

        Parameters:
        chunks (list): The text chunks.

        Returns:
        list: The embeddings.

        """
        pass


class DefaultTextProcessor(TextProcessor):
    """Default text processor."""

    def __init__(self, param_controller):
        self.param_controller = param_controller

    def split_text(self, text):
        """Split the text into chunks.

        Parameters:
        text (str): The text to split.

        Returns:
        list: The text chunks.
        """

        #### PRE- SET UP CHUNK CONFIGS
        chunk_size = self.param_controller.get_parameter('chunk_size')['value']
        chunk_overlap = self.param_controller.get_parameter('chunk_overlap')['value']

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap, 
            separators=[" ", ",", "\n"],
            length_function=len
        )

        chunks = text_splitter.split_text(text)
        return chunks

    def create_embeddings(self, chunks):
        """Create embeddings from the text chunks.

        Parameters:
        chunks (list): The text chunks.

        Returns:
        list: The embeddings.

        """
        #### can this function be called without any chunks?
        if not chunks:
            return None
        embeddings = OpenAIEmbeddings()
        try:
            return FAISS.from_texts(chunks, embeddings)
        except Exception as e:
            print(f"Error creating embeddings: {e}")
            return None
