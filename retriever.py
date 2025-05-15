#!/usr/bin/env python3
"""
Retriever module for loading relevant documents from a ChromaDB vector store
using semantic similarity search with OpenAI embeddings.
"""

import os
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document

try:
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma
except ImportError:
    raise ImportError(
        "Required packages not installed. Please run: "
        "pip install langchain-openai langchain-community"
    )

# Load environment variables (including OPENAI_API_KEY)
load_dotenv()


def load_docs(query: str, k: int = 5) -> List[Document]:
    """
    Retrieve the most relevant documents from the Chroma vector store based on a query.

    Args:
        query (str): The search query text
        k (int, optional): Number of documents to retrieve. Defaults to 5.

    Returns:
        List[Document]: A list of Document objects containing the most relevant text chunks.
                        Each Document has page_content and metadata attributes.

    Example:
        >>> docs = load_docs("What is the project MVP?")
        >>> for doc in docs:
        >>>     print(doc.page_content)
    """
    # Check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(
            "OPENAI_API_KEY environment variable not found. Make sure it's set in your .env file."
        )

    # Path to the persisted Chroma database
    chroma_dir = "./chroma_index"

    # Check if the Chroma index exists
    if not os.path.exists(chroma_dir):
        raise FileNotFoundError(
            f"Chroma index not found at {chroma_dir}. Please run the indexing script first."
        )

    # Initialize the embedding model
    embeddings = OpenAIEmbeddings()

    # Load the existing Chroma vector store
    vectordb = Chroma(persist_directory=chroma_dir, embedding_function=embeddings)

    # Create a retriever from the vector store
    retriever = vectordb.as_retriever(search_kwargs={"k": k})

    # Retrieve relevant documents
    docs = retriever.invoke(query)

    return docs


# Example code is commented out to avoid the "pointless string statement" warning
# Example usage:
# docs = load_docs("O que é o MVP do projeto?")
# for i, doc in enumerate(docs):
#     print(f"Trecho {i+1}:", doc.page_content)
