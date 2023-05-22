from abc import ABC, abstractmethod
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


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
