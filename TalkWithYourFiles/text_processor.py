from abc import ABC, abstractmethod
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

"""
In this file Strategy Design Pattern is used to make this functionalities more flexible & maintainable.
Currently there's only one text processor subclass which is called DefaultTextProcessor.

If you met the need to extend this further by adding a new text processor subclass:
1) Create a new subclass of TextProcessor in this file.
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

    def split_text(self, text):
        """Split the text into chunks.

        Parameters:
        text (str): The text to split.

        Returns:
        list: The text chunks.

        """
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        return text_splitter.split_text(text)

    def create_embeddings(self, chunks):
        """Create embeddings from the text chunks.

        Parameters:
        chunks (list): The text chunks.

        Returns:
        list: The embeddings.

        """
        if not chunks:
            return None
        embeddings = OpenAIEmbeddings()
        try:
            return FAISS.from_texts(chunks, embeddings)
        except Exception as e:
            print(f"Error creating embeddings: {e}")
            return None
