import chromadb
from langchain.docstore.document import Document
from langchain.vectorstores.chroma import Chroma
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
import os
import shutil


CHROMA_PATH = "./chroma_db"
DATA_PATH = "data"

openai_api_key = os.getenv("OPENAI_API_KEY")


def main():
    generate_data_store()


def generate_data_store():
    """
    Generating data storage
    - loading documents -> load_documents function
    - splitting to chunks -> split_text function
    - saving it to chroma folder

    """
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    """
    Loading documents

    output:
    documents
    """
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    """
    splitting document`s text into chunks where
    chunk_size = number of characters
    chank_overlap = number overlapping characters in chunks

    Args:
        document (text data from DATA_PATH)

    Return:
        chunks from from splitted documents
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    chunks = [
        Document(page_content=doc.page_content, metadata={"topic": f"python doc {i}"})
        for i, doc in enumerate(chunks)
    ]
    return chunks


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        chunks,
        OpenAIEmbeddings(openai_api_key=openai_api_key),
        persist_directory=CHROMA_PATH,
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
