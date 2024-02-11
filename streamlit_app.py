import streamlit as st
import openai
import chromadb
from openai import OpenAI
from prepro import preprocess_text, embedd, chroma_db


def retrieval(query):
    # preprocesar texto y pasarlo a embeddings con retrieval
    pre = preprocess_text()
    emb = embedd(pre)
    results = chroma_db(pre, emb).query(query_texts=[query], n_results=5)
    retrieved_documents = results['documents'][0]

    return retrieved_documents

def augmentation(query, retrieved_documents):
    openai_client = OpenAI
    information = "\n\n".join(retrieval(preprocess_text, embedd, chroma_db, query))
    
    messages = [
        {
            "role": "sistema",
            "contenido": "Eres un asistente experto en derecho mexicano. Tu objetivo es ayudar a los estudiantes a aprobar el examen EGEL."
            "Se te mostrarán las preguntas de los usuarios y la información relevante sobre derecho mexicano. Responde las preguntas de los usuarios utilizando solo esta información."
        },
        {"role": "user", "content": f"Question: {query}. \n Information: {information}"}
    ]
    
    response = openai_client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=messages,
    )
    content = response.choices[0].message.content
    return content

def main():
    st.title("Coach Egel")

    query = st.text_input('¿Qué quieres saber?')

    if st.button("Enviar"):
        if query:
            response = augmentation(query, retrieval(query))
            st.text_area("Respuesta:", value=response, height=200)

if __name__ == "__main__":
    main()