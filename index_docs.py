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
    # Check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(
            "OPENAI_API_KEY environment variable not found. Make sure it's set in your .env file."
        )

    # Set path variables
    docs_dir = "./docs"
    chroma_dir = "./chroma_index"

    # Create the chroma directory if it doesn't exist
    os.makedirs(chroma_dir, exist_ok=True)

    # Load all markdown files from the docs directory
    print(f"🔍 Loading markdown files from {docs_dir}...")
    loader = DirectoryLoader(
        docs_dir,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()

    if not documents:
        print("⚠️ No markdown files found in the docs directory.")
        return

    print(f"📄 Found {len(documents)} document(s).")

    # Split the documents into chunks
    print("✂️ Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)

    print(f"🧩 Created {len(chunks)} chunks.")

    # Initialize OpenAI embeddings
    print("🔤 Initializing OpenAI embeddings...")
    embeddings = OpenAIEmbeddings()

    # Create and persist the vector database
    print("💾 Creating and persisting vector database...")
    vectordb = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=chroma_dir
    )

    # Persist the database
    vectordb.persist()

    print(f"✅ Base indexed with success! Stored in {chroma_dir}")


if __name__ == "__main__":
    index_markdown_files()
