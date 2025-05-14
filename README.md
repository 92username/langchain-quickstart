![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Bash Script](https://img.shields.io/badge/bash_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)



![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) 

![Docker Image Size](https://img.shields.io/docker/image-size/user92/langchain-quickstart/latest) ![Docker Pulls](https://img.shields.io/docker/pulls/user92/langchain-quickstart) 

![Python](https://img.shields.io/badge/python-3.13-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.25.0-ff4b4b)

[![CI - Code Quality and Security](https://github.com/92username/langchain-quickstart/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/92username/langchain-quickstart/actions/workflows/ci.yml)
[![CD - Deploy VPS](https://github.com/92username/langchain-quickstart/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/92username/langchain-quickstart/actions/workflows/deploy.yml) 

# EstudaMais.tech

**EstudaMais.tech** é uma plataforma experimental que integra inteligência artificial e ferramentas educacionais para apoiar estudantes universitários, com foco inicial em alunos da Estácio. O projeto está em fase de _Closed Beta_.


## ℹ️ Sobre o Projeto

Esta aplicação fornece um assistente baseado em IA treinado para responder dúvidas sobre:

- GitHub Student Pack (GHSP)
- Recursos gratuitos para estudantes
- A própria plataforma EstudaMais.tech e seus benefícios

A proposta central é ajudar o estudante a transformar tempo de estudo em valor investido na própria carreira, aproveitando recursos gratuitos oferecidos por instituições e empresas de tecnologia.

---

## 👤 Para Usuários Finais

### Como utilizar

Acesse:  
[https://estudamais.tamanduas.dev](https://estudamais.tamanduas.dev)

O assistente está disponível diretamente via navegador.  
Não é necessário cadastro ou login. Basta inserir sua pergunta e interagir com a IA.

### Avisos

- Esta versão é um _Closed Beta_, destinada a testes.
- As conversas podem ser registradas para fins de melhoria contínua da plataforma.
- Não envie informações sensíveis como nome completo, documentos ou senhas.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.11](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [GitHub Actions](https://docs.github.com/actions)
- [Nginx](https://nginx.org/)
- [Certbot](https://certbot.eff.org/) (Let's Encrypt)
- [OpenAI API](https://platform.openai.com/)
- Linux Ubuntu Server (Hostinger VPS)

---

## 🧑‍💻 Para Desenvolvedores

### Clonando o repositório

```bash
git clone https://github.com/92username/langchain-quickstart.git
cd langchain-quickstart
```

### Variáveis de ambiente

Crie um arquivo `.env` com a seguinte variável:

```env
OPENAI_API_KEY=your_openai_api_key
```

### Executando localmente via Docker Compose

```bash
docker compose up --build
```

O aplicativo estará disponível em [http://localhost:8501](http://localhost:8501)

> Observação: o log das conversas será salvo em `logs/conversas.csv`. Esse volume é persistente entre builds.

---

## 🚀 CI/CD

Este projeto está configurado com pipeline de integração e entrega contínua (CI/CD) utilizando **GitHub Actions**.

A cada `push` na branch `main`, é realizado automaticamente:

* Build da imagem Docker
* Push da imagem para o Docker Hub
* Deploy remoto via SSH na VPS
* Reinicialização do container com o código mais recente

> Para detalhes técnicos sobre a pipeline CI/CD, veja o arquivo [`CI-CD.md`](./CI-CD.md) (Em desenvolvimento)

---
