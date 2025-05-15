#!/usr/bin/env python3
"""
Estudamais.tech Chatbot Interface.

This Streamlit application provides an interactive chatbot for students,
focusing on information about Estudamais.tech, GitHub, GitHub Student Pack,
and related educational topics.
"""

import os
import csv
from datetime import datetime

import streamlit as st
from streamlit_modal import Modal
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Import the retriever function instead of the loader
from retriever import load_docs

# Import the custom logger
from logger import logger, error, info, warning

# Load environment variables
load_dotenv()

# Configuração da página - DEVE SER O PRIMEIRO COMANDO ST
st.set_page_config(page_title="Estudamais.tech")

# Apply custom CSS with gradient background and improved typography
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #1c4145, #457a8e);
        color: #f8f8f8;
    }
    
    h1, h2, h3 {
        color: #e5e5e5;
    }
    
    .stButton button {
        background-color: #1e88e5;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton button:hover {
        background-color: #0d47a1;
    }
    
    .stChat {
        border-radius: 10px;
    }
    
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 5px;
    }
    
    .stChatInputContainer {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 5px;
    }
    
    a {
        color: #64b5f6;
    }
    
    a:hover {
        color: #bbdefb;
    }
    
    /* Estilos para o sidebar */
    .css-1d391kg, .css-1wrcr25, .css-ocqkz7 {  /* Classes do sidebar no Streamlit */
        background-color: #1c4145 !important;
    }
    
    .css-pkbazv {  /* Classe para links do sidebar */
        color: #64b5f6 !important;
    }
    
    .css-pkbazv:hover {
        color: #bbdefb !important;
    }
    
    /* Se você quiser um gradiente no sidebar similar ao fundo principal */
    [data-testid="stSidebar"] {
        background: linear-gradient(175deg, #1c4145, #2a606a) !important;
        color: #f8f8f8 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Logging application start
info("Aplicação Estudamais.tech iniciada")

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Inicializar o modal de boas-vindas com a biblioteca streamlit-modal
modal = Modal(key="welcome_modal", title="Bem-vindo à EstudaMais!")
modal_open = not st.session_state.get("popup_exibido", False)

if modal_open:
    with modal.container():
        st.markdown(
            """
        👋 Olá! Antes de começar a conversar com a nossa IA, leia com atenção:

        - Esta ferramenta é voltada para estudantes da **Estácio**
        - O foco da IA é **a startup Estudamais.tech, Github, GitHub Student Pack
          e temas relacionados**
        - **Não envie dados sensíveis**, como: nome completo, número de documentos ou senhas
        - As perguntas podem ser registradas para fins de melhoria contínua da plataforma

        Clique no botão abaixo para continuar.
        """
        )
        if st.button("Entendi"):
            st.session_state["popup_exibido"] = True
            st.rerun()

# Garantir que a pasta de logs existe
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
    info(f"Diretório de logs criado: {logs_dir}")

# Verificar se o arquivo CSV existe, caso contrário criar com cabeçalho
csv_file = os.path.join(logs_dir, "conversas.csv")
if not os.path.exists(csv_file):
    with open(csv_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "pergunta", "resposta"])
    info(f"Arquivo de conversas criado: {csv_file}")

# Título e descrição do aplicativo
st.title(
    "Estudamais.tech - A startup que quer investir mais de  R$1.000.000,00 na sua carreira!"
)
st.markdown(
    "<h3 style='text-align: center; font-size: 1.2em;'>Converse comigo para saber mais 👇</h3>",
    unsafe_allow_html=True,
)

# Carregando a API key do ambiente ao invés de solicitar do usuário
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    warning("OPENAI_API_KEY não encontrada no ambiente")

# Adicionando seção de links úteis no sidebar
st.sidebar.markdown(
    """
## 🧪 Este é um Closed Beta

Este aplicativo está em fase de desenvolvimento.
Se você está visualizando esta mensagem, é porque foi convidado(a) a testar e contribuir com a evolução da plataforma.

A equipe da EstudaMais.tech agradece seu apoio e feedback!
"""
)
st.sidebar.markdown("---")
# Placeholders para links futuros
st.sidebar.markdown("[🏢 Site da EstudaMais](https://estudamais.com)")
st.sidebar.markdown(
    "[💻 GitHub da EstudaMais](https://github.com/92username/langchain-quickstart)"
)
st.sidebar.markdown("[📱 Contato via WhatsApp](https://wa.me/seunumero)")
st.sidebar.markdown("[❓ Perguntas Frequentes (FAQ)](https://estudamais.com/faq)")
st.sidebar.markdown("[📃 Termos de Uso](https://estudamais.com/termos)")

# Mensagem de sistema para dar identidade ao chatbot
system_message = """
## Identidade
Você é a Luiza, a assistente virtual da EstudaMais.tech — uma plataforma que ajuda estudantes universitários a desbloquear o máximo dos benefícios do GitHub Student Pack. 
Você é animada, prestativa, acolhedora e gosta de explicar as coisas com entusiasmo, como se estivesse torcendo pelo sucesso do usuário. Use um tom leve e otimista, mas mantenha a precisão das informações.
Evite parecer robótica ou formal demais.


## Missão
Guiar estudantes universitários sobre:
• GitHub Student Developer Pack (GHSP)  
• Ferramentas gratuitas/educacionais  
• Oportunidades na Estácio e na EstudaMais  

## Fontes
1. Use primeiro o **conteúdo relevante** de /docs (resumos fornecidos pelo system).  
2. Complementar com conhecimento geral confiável quando necessário.

## Estilo
• Linguagem acessível e motivadora, porém direta.  
• Máx. **3 parágrafos ou 200 palavras** (salvo pedido do usuário).  
• Use listas com `-` se melhorar a clareza.  
• Cite exemplos práticos sempre que possível.

## Política
Se não souber, responda "Não tenho essa informação no momento" e ofereça canal de contato.  
Nunca invente dados numéricos.

(⬇️ o sistema injeta aqui o contexto retornado pelo mecanismo de retrieval)
"""


def generate_response(input_text):
    """
    Generate a response using RAG (Retrieval-Augmented Generation) based on user input.

    This function:
    1. Retrieves relevant document chunks from ChromaDB based on the query
    2. Uses these documents as context for the LLM
    3. Displays both the response and source documents used

    Args:
        input_text (str): The user's query text

    Returns:
        str: The generated response text
    """
    # Check for API key
    if not openai_api_key:
        error("Tentativa de gerar resposta sem API key configurada")
        st.error("OpenAI API key is required!")
        return None

    # Log the query received
    info(f"Pergunta recebida: {input_text[:50]}...")

    # Get relevant documents from ChromaDB using the retriever
    try:
        with st.spinner("Luiza está pensando..."):
            # Log retrieval attempt
            info("Buscando documentos relevantes na base de conhecimento...")

            retrieved_docs = load_docs(input_text, k=5)

            if not retrieved_docs:
                warning("Nenhum documento relevante encontrado para a consulta")
                context = "No specific context available."
            else:
                # Create a concatenated context from the retrieved documents
                context = "\n\n".join([doc.page_content for doc in retrieved_docs])
                info(f"Encontrados {len(retrieved_docs)} documentos relevantes")

            # Initialize the LLM
            info("Inicializando modelo de linguagem...")
            llm = ChatOpenAI(
                model_name="gpt-4.1-nano",  # or "gpt-4o"
                temperature=0.7,
                max_tokens=700,
                api_key=openai_api_key,
            )

            # Create messages with system context and user input
            messages = [
                {"role": "system", "content": system_message + "\n\n" + context},
                {"role": "user", "content": input_text},
            ]

            # Generate response
            info("Gerando resposta com o modelo...")
            response = llm.invoke(messages)
            response_content = response.content
            info("Resposta gerada com sucesso")

        # Show sources in an expander if we have retrieved documents
        if retrieved_docs:
            with st.expander("📚 Fontes utilizadas"):
                for i, doc in enumerate(retrieved_docs):
                    st.markdown(f"**Fonte {i+1}:**")
                    st.markdown(f"```\n{doc.page_content}\n```")
                    if hasattr(doc, "metadata") and doc.metadata:
                        source = doc.metadata.get("source", "Desconhecida")
                        st.caption(f"Fonte: {source}")
                    st.markdown("---")

        # Log the conversation
        try:
            with open(csv_file, mode="a", encoding="utf-8", newline="") as log_file:
                log_writer = csv.writer(log_file)
                log_writer.writerow([datetime.now(), input_text, response_content])
                info("Conversa registrada no arquivo CSV")
        except IOError as e:
            error(f"Erro ao registrar conversa no arquivo CSV: {e}", exc_info=True)

        return response_content

    except Exception as e:
        error_message = f"Erro ao gerar resposta: {str(e)}"
        error(error_message, exc_info=True)

        # Provide a user-friendly error message
        st.error(
            "Desculpe, ocorreu um erro interno. Nossa equipe foi notificada e está trabalhando para resolver o problema."
        )

        # For development environment, you can show more details
        if os.getenv("ENVIRONMENT") == "development":
            import traceback

            st.error(traceback.format_exc())

        return None


# API key warning if not configured
if not openai_api_key or not openai_api_key.startswith("sk-"):
    st.warning(
        "Chave da API OpenAI não encontrada. Verifique o arquivo .env!", icon="⚠"
    )
    warning("API Key OpenAI ausente ou em formato inválido")

# Display welcome message if chat history is empty
if not st.session_state.chat_history:
    with st.chat_message("assistant"):
        st.markdown(
            "Olá! Sou a Luiza, assistente virtual da EstudaMais.tech. Como posso ajudar você hoje?"
        )

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input with chat_input
user_input = st.chat_input("Digite sua mensagem...")

if user_input:
    # Add user message to chat history and display it
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    response = generate_response(user_input)

    if response:
        # Add assistant response to chat history and display it
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
