import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

#Llave de openai
OPEN_AI_KEY = "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"

EMBEDDING_MODEL = "text-embedding-3-small"
embedding_function = OpenAIEmbeddingFunction(api_key=OPEN_AI_KEY, model_name=EMBEDDING_MODEL)

def load_text(path="data/documents/datos.txt"):
    # List files
    test = []
    with open(path, "r") as reader:
        for lines in reader:
            test.append(lines)
    return test

def split_doc(documents, chunk_size = 200, chunk_overlap = 0):
    character_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ". ", " ", ""],
    chunk_size=400,
    chunk_overlap=0
)
    character_split_texts = character_splitter.split_text('\n\n'.join(documents))
    return character_split_texts

def embed_chunk(chunks, embedding=embedding_function):
    print("Embedding chunks...")
    chroma_client = chromadb.PersistentClient(path="data/chroma_db")
    chroma_collection = chroma_client.create_collection("documento_preprocesado", embedding_function=embedding)
    
    return chroma_collection



if __name__ == "__main__":
    documents = load_text()
    chunks = split_doc(documents)
    embed_chunk(chunks)