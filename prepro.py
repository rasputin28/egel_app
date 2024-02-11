import openai
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# llave openai
key = "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"
# modelo de embeddings
EMBEDDING_MODEL = "text-embedding-3-small"

# preprocesamiento de texto
def preprocess_text():
    
    # instanciar datos
    with open("egel_app/datos.txt", "r") as file:
        text = file.read()

    character_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ". ", " ", ""],
    chunk_size=400,
    chunk_overlap=0
)
    character_split_texts = character_splitter.split_text('\n\n'.join(text))
    return character_split_texts

#sacar los embeddings del texto preprocesado
def embedd(character_split_texts):
    
    embedding_function = OpenAIEmbeddingFunction(api_key=key, model_name=EMBEDDING_MODEL)
    return embedding_function(character_split_texts)
    

def chroma_db(character_split_texts, embedding_function):
    chroma_client = chromadb.Client()
    chroma_collection = chroma_client.create_collection("egel", embedding_function=embedding_function)

    ids = [str(i) for i in range(len(character_split_texts))]

    chroma_collection.add(ids=ids, documents=character_split_texts)
    
    return chroma_collection
