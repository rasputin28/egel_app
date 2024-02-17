from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import openai
from openai import OpenAI



OPEN_AI_KEY = "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"
embeddings_model = OpenAIEmbeddings(openai_api_key=OPEN_AI_KEY)
model = "gpt-3.5-turbo"
openai_client = OpenAI(api_key = OPEN_AI_KEY)

def get_chunks(question):
  loaded_vectordb = Chroma(persist_directory="data/chroma_db", embedding_function=embeddings_model)
  docs = loaded_vectordb.max_marginal_relevance_search(question, k=4)
  chunks = ' '.join([chunk.page_content for chunk in docs])
  return chunks

def answer_question(chunks, question, history):
    
    information = "\n\n".join(chunks)

    messages = [
        {
            "role": "system",
            "content": "Eres un asistente experto en derecho mexicano. Tu objetivo es ayudar a los estudiantes a aprobar el examen EGEL."
            "Se te mostrarán las preguntas de los usuarios y la información relevante sobre derecho mexicano. Responde las preguntas de los usuarios utilizando solo esta información."

        },
        {"role": "user", "content": f"Question: {question}. \n Information: {information + history}"}
    ]

    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
    )
    content = response.choices[0].message.content
  
    return content
    
