#!/usr/bin/env python3
"""
Retriever module for loading relevant documents from a ChromaDB vector store
using semantic similarity search with OpenAI embeddings.
"""

import os
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document

# Import logger for detailed error tracking
try:
    from logger import logger, info, warning, error
except ImportError:
    # Fallback to basic logging if logger module is not available
    import logging

    logger = logging.getLogger(__name__)
    info = logger.info
    warning = logger.warning
    error = logger.error

try:
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma
except ImportError:
    error_msg = "Required packages not installed. Please run: pip install langchain-openai langchain-community"
    try:
        error(error_msg)
    except (NameError, AttributeError) as e:
        # Exceções específicas para quando error() não está definido ou não é uma função
        print(f"Logging unavailable: {error_msg}")
    raise ImportError(error_msg)

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
    info(f"Buscando documentos para a query: '{query[:50]}...' (k={k})")

    try:
        # Check if OPENAI_API_KEY is set
        if not os.getenv("OPENAI_API_KEY"):
            error_msg = "OPENAI_API_KEY environment variable not found. Make sure it's set in your .env file."
            error(error_msg)
            raise ValueError(error_msg)

        # Path to the persisted Chroma database
        chroma_dir = "./chroma_index"

        # Check if the Chroma index exists
        if not os.path.exists(chroma_dir):
            error_msg = f"Chroma index not found at {chroma_dir}. Please run the indexing script first."
            error(error_msg)
            raise FileNotFoundError(error_msg)

        # Initialize the embedding model
        info("Inicializando modelo de embeddings...")
        embeddings = OpenAIEmbeddings()

        # Load the existing Chroma vector store
        info(f"Carregando base vetorial de {chroma_dir}")
        vectordb = Chroma(persist_directory=chroma_dir, embedding_function=embeddings)

        # Create a retriever from the vector store
        retriever = vectordb.as_retriever(search_kwargs={"k": k})

        # Retrieve relevant documents
        info("Realizando busca semântica...")
        docs = retriever.invoke(query)

        info(f"Busca concluída. Encontrados {len(docs)} documentos relevantes.")
        return docs

    except Exception as e:
        error(f"Erro ao recuperar documentos do ChromaDB: {str(e)}", exc_info=True)
        # Re-raise exception for appropriate handling by caller
        raise


# Example code is commented out to avoid the "pointless string statement" warning
# Example usage:
# docs = load_docs("O que é o MVP do projeto?")
# for i, doc in enumerate(docs):
#     print(f"Trecho {i+1}:", doc.page_content)
