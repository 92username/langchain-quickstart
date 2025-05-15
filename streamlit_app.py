import streamlit as st
from streamlit_modal import Modal
from langchain_openai import ChatOpenAI  # fake commit to triger a new build
import os
from dotenv import load_dotenv
import csv
from datetime import datetime
from loader import load_docs

# Carregar variáveis do arquivo .env
load_dotenv()

# Configuração da página
st.set_page_config(page_title="Estudamais.tech")

# Inicializar o modal de boas-vindas com a biblioteca streamlit-modal
modal = Modal(key="welcome_modal", title="Bem-vindo à EstudaMais!")
modal_open = not st.session_state.get("popup_exibido", False)

if modal_open:
    with modal.container():
        st.markdown(
            """
        👋 Olá! Antes de começar a conversar com a nossa IA, leia com atenção:

        - Esta ferramenta é voltada para estudantes da **Estácio**
        - O foco da IA é **a startup Estudamais.tech, Github, GitHub Student Pack e temas relacionados**
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

# Verificar se o arquivo CSV existe, caso contrário criar com cabeçalho
csv_file = os.path.join(logs_dir, "conversas.csv")
if not os.path.exists(csv_file):
    with open(csv_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "pergunta", "resposta"])

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
st.sidebar.markdown("[💻 GitHub da EstudaMais](https://github.com/estudamais)")
st.sidebar.markdown("[📱 Contato via WhatsApp](https://wa.me/seunumero)")
st.sidebar.markdown("[❓ Perguntas Frequentes (FAQ)](https://estudamais.com/faq)")
st.sidebar.markdown("[📃 Termos de Uso](https://estudamais.com/termos)")

# Mensagem de sistema para dar identidade ao chatbot
system_message = """
## Identidade
Você é **Luiza**, a assistente educacional da plataforma EstudaMais.tech.

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
    # Carregar o contexto dos documentos
    context = load_docs()

    # Construir mensagens com sistema + contexto e input do usuário
    messages = [
        {"role": "system", "content": system_message + "\n\n" + context},
        {"role": "user", "content": input_text},
    ]

    # Criar instância do modelo
    llm = ChatOpenAI(
        model_name="gpt-4.1-nano",  # ou "gpt-4o"
        temperature=0.5,
        api_key=openai_api_key,
    )

    # Invocar o modelo
    response = llm.invoke(messages)
    response_content = response.content

    # Registrar a conversa no log
    with open(csv_file, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), input_text, response_content])

    # Exibir resposta
    st.info(response_content)


with st.form("my_form"):
    text = st.text_area("Digite aqui:", "Quero saber mais sobre a Estudamais.tech")
    submitted = st.form_submit_button("Enviar")
    if not openai_api_key or not openai_api_key.startswith("sk-"):
        st.warning(
            "Chave da API OpenAI não encontrada. Verifique o arquivo .env!", icon="⚠"
        )
    elif submitted:
        generate_response(text)
