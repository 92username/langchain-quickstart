#!/usr/bin/env python3
"""
Document Indexing module for LangChain RAG System.

This script reads markdown files from a directory, splits them into chunks,
generates embeddings using OpenAI, and stores them in a local ChromaDB vector store
for later retrieval and querying with LLMs.
"""

import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.text import TextLoader
from dotenv import load_dotenv

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

# Load environment variables (including OPENAI_API_KEY)
load_dotenv()


def index_markdown_files():
    """
    Index all markdown files in the ./docs directory:
    1. Load all .md files
    2. Split content into chunks
    3. Generate embeddings with OpenAI
    4. Store vectors in ChromaDB
    """
    info("Iniciando processo de indexação de documentos...")
    try:
        # Check if OPENAI_API_KEY is set
        if not os.getenv("OPENAI_API_KEY"):
            error_msg = "OPENAI_API_KEY environment variable not found. Make sure it's set in your .env file."
            error(error_msg)
            raise ValueError(error_msg)

        # Set path variables
        docs_dir = "./docs"
        chroma_dir = "./chroma_index"

        # Create the chroma directory if it doesn't exist
        os.makedirs(chroma_dir, exist_ok=True)
        info(f"Diretório de índice criado/verificado: {chroma_dir}")

        # Load all markdown files from the docs directory
        info(f"Carregando arquivos markdown de {docs_dir}...")
        loader = DirectoryLoader(
            docs_dir,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        documents = loader.load()

        if not documents:
            warning("Nenhum arquivo markdown encontrado no diretório de documentos.")
            return

        info(f"Encontrados {len(documents)} documento(s).")

        # Split the documents into chunks
        info("Dividindo documentos em chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
        )
        chunks = text_splitter.split_documents(documents)

        info(f"Criados {len(chunks)} chunks.")

        # Initialize OpenAI embeddings
        info("Inicializando embeddings OpenAI...")
        embeddings = OpenAIEmbeddings()

        # Create and persist the vector database
        info("Criando e persistindo banco de dados vetorial...")
        vectordb = Chroma.from_documents(
            documents=chunks, embedding=embeddings, persist_directory=chroma_dir
        )

        # Persist the database
        vectordb.persist()

        info(f"Base indexada com sucesso! Armazenada em {chroma_dir}")
    
    except Exception as e:
        error(f"Erro durante a indexação: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        index_markdown_files()
    except Exception as e:
        error(f"Falha na execução principal: {str(e)}", exc_info=True)
        print(f"❌ Erro ao indexar documentos: {str(e)}")
        print("Consulte os logs para mais detalhes.")
