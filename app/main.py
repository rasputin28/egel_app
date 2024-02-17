import streamlit as st
from langchain.llms import OpenAI 
from helper import get_chunks, answer_question

# valid_passwords = {
#     "1": "Administrator"}

# # Page for login
# def login_page():
#     st.image("https://www.revistaabogacia.com/wp-content/uploads/2023/09/Retos-de-la-abogacia.webp", width=800)
#     st.title("Iniciar Sesión")
#     st.write("Bienvenido al chatbot de Coach Académico Egel. Por favor, ingresa tu clave de acceso para continuar.")
#     password = st.sidebar.text_input("Clave de acceso", type="password")
#     if st.sidebar.button("Ingresa tu clave de acceso"):
#         if password in valid_passwords:
#             st.session_state["user_type"] = valid_passwords[password]
#             st.experimental_rerun()
#         else:
#             st.error("Clave inválida. Inténtalo de nuevo.")

st.image("https://miguelcarbonell.me/wp-content/uploads/2023/06/Una-abogacia-disruptiva.jpg", width=800)
st.title("Coach Académico Egel")
st.subheader("¡Bienvenido! Soy tu asistente virtual para ayudarte a prepararte para el examen EGEL. ¿En qué puedo ayudarte hoy?")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant",
                                  "content": "Hola, soy tu coach EGEL. ¿En qué puedo ayudarte?"}]
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Pregúntame"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    history = " ".join([f""" "Role":"{msg["role"]}" \n "Content": "{msg["content"]}" """ for msg in st.session_state.messages])

    # Bot answer
    with st.chat_message("assistant"):
        # Get relevant chunks
        chunks = get_chunks(
            question=prompt
            )
        
        # Get bot answer
        answer = answer_question(
            question=prompt,
            chunks=chunks,
            history=history
            )
    
    st.chat_message("assistant").markdown(answer)

    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})