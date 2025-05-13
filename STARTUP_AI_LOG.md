# 📘 Startup Log – EstudaMais Chatbot

Este documento registra a evolução técnica do chatbot educacional da EstudaMais, desde o fork inicial até o estágio atual de desenvolvimento.

---

## 🧩 Etapa 1 – Fork e ambiente local

- O projeto começou a partir de um fork do repositório [langchain-ai/langchain-quickstart](https://github.com/langchain-ai/langchain-quickstart).
- O objetivo inicial era testar um template básico de chatbot em Streamlit utilizando modelos da OpenAI.

**Modificações iniciais:**
- Remoção do campo de entrada manual da OpenAI API Key.
- Leitura da chave via `.env` usando a biblioteca `python-dotenv`.
- Customização do painel lateral com links úteis da startup (site, GitHub, contato, etc.).

---

## 🔁 Etapa 2 – Correções e atualização da stack

**Problemas corrigidos:**
- O código original utilizava `from langchain.llms import OpenAI`, que foi depreciado.
- Migramos para `langchain-openai` com uso da classe `ChatOpenAI` e o método `.invoke()`.

**Dependências atualizadas:**
```txt
streamlit>=1.25.0
langchain-openai>=0.1.6
langchain-core>=0.1.30
python-dotenv>=1.0.0
openai
streamlit-modal>=0.1.2
```

---

## 🧠 Etapa 3 – Injeção de contexto via arquivos Markdown

- Criamos a pasta `docs/` para armazenar arquivos `.md` com informações úteis da startup e do GitHub Student Pack.
- Foi desenvolvido o script `loader.py`, que lê e concatena os arquivos de forma automática.
- Esse conteúdo é injetado como contexto no `system_message` do prompt enviado à LLM.

---

## 💬 Etapa 4 – Interface interativa com aviso inicial

- O modal nativo `st.modal()` apresentou problemas de compatibilidade.
- Solução adotada: a biblioteca `streamlit-modal`, que funciona com qualquer versão recente do Streamlit.
- Criado um aviso institucional com boas práticas de uso e alerta de privacidade.

---

## 📦 Etapa 5 – Logs das interações

- Criado o diretório `logs/` com o arquivo `conversas.csv`.
- Cada pergunta e resposta é registrada com `timestamp`, via módulo `csv`.
- O arquivo está listado no `.gitignore`, mas a estrutura da pasta é mantida com um `.gitkeep`.

---

## 🔧 Tech Stack atual (até o momento)

| Categoria         | Ferramenta           |
|-------------------|----------------------|
| 🧠 LLM             | OpenAI (GPT-4o)      |
| 💬 Interface       | Streamlit            |
| 📦 Empacotamento   | Docker (em preparação) |
| 🧱 Base            | Template LangChain Quickstart |
| 📁 Contexto        | Markdown (`.md`)     |
| 🗃️ Log             | CSV (`logs/conversas.csv`) |
| ⚙️ Ambiente        | Python 3.12 + venv    |

---

## 🛠️ Próximos passos (previstos)

- Criar `docker-compose.yml` com persistência dos logs
- Configurar deploy na VPS da Hostinger
- Implementar sistema de feedback por pergunta (👍 / 👎)
- Criar seção de FAQ baseada nos logs mais frequentes

---

*Documento mantido manualmente por Vinicius — atualizado em 13/05/2025*
