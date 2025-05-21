[![CI - Code Quality and Security](https://github.com/92username/langchain-quickstart/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/92username/langchain-quickstart/actions/workflows/ci.yml)
[![CD - Deploy VPS](https://github.com/92username/langchain-quickstart/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/92username/langchain-quickstart/actions/workflows/deploy.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/d765b1d13b02475097a2dc081cebab54)](https://app.codacy.com/gh/92username/langchain-quickstart/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

![Docker Image Size](https://img.shields.io/docker/image-size/user92/langchain-quickstart/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/user92/langchain-quickstart)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge\&logo=python\&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge\&logo=streamlit\&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge\&logo=docker\&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge\&logo=nginx\&logoColor=white)
![LangChain](https://img.shields.io/badge/langchain-0E1117?style=for-the-badge\&logo=data\&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge\&logo=githubactions\&logoColor=white)

---

# EstudaMais.tech – Generative AI Infrastructure with RAG and Automated Deployment

This repository implements a complete stack for an educational chatbot powered by **Generative AI**, using a **Retrieval-Augmented Generation (RAG)** architecture, **Docker Compose**, **Streamlit**, **LangChain**, **GitHub Actions**, and automated deployment to a VPS using **Nginx + HTTPS** via **Certbot**.

The AI assistant, codenamed **Luiza**, answers questions based on a local knowledge base built from Markdown files, combining vector search with OpenAI-generated responses.

---

## 🔍 Architecture and Components

### Retrieval-Augmented Generation (RAG)

* **LangChain Retriever** using embedded `ChromaDB`
* Embeddings are generated on boot from `.md` files in the `/docs` folder
* Integration with `RetrievalQA` and `OpenAI` (configurable model)

### Containerization & Deployment

* **Dockerfile** based on `python:3.13-slim`
* **docker-compose.yml** orchestrates app + Nginx
* HTTPS reverse proxy via **Certbot**
* Persistent volume for CSV-based structured logs
* Automated deployment to a VPS using **CI/CD**

### CI/CD

* GitHub Actions pipeline performs:

  * Code linting with `ruff`, `bandit`, `mypy`
  * Docker image build
  * Push to Docker Hub
  * Remote deployment via SSH + `docker compose up`

---

## 📂 Project Structure

```bash
.
├── .github/workflows/        # CI/CD Pipelines
├── /docs/                    # Markdown knowledge base (indexed with ChromaDB)
├── /logs/                    # CSV logs of user queries
├── retriever.py              # Document loader and embedder
├── streamlit_app.py          # Main application interface
├── docker-compose.yml        # Service orchestration
├── Dockerfile                # Main Docker image
├── redeploy.sh               # Manual restart script for VPS
└── .env                      # OpenAI API key
```

---

## ⚙️ Running Locally

1. Clone the repository:

```bash
git clone https://github.com/92username/langchain-quickstart.git
cd langchain-quickstart
```

2. Create a `.env` file with your OpenAI key:

```env
OPENAI_API_KEY=sk-xxxxx
```

3. Run with Docker Compose:

```bash
docker compose up --build
```

> The application will be available at `http://localhost:8501`

---

## 🔐 Production

The production environment runs on a VPS (Hostinger) and is accessible via:

**[https://estudamais.tamanduas.dev](https://estudamais.tamanduas.dev)**

* Secure HTTPS requests
* Reverse proxy via Nginx
* Automated deployment via GitHub Actions

---

## 📈 Observability & Logging

* All user questions are logged in `logs/conversas.csv`
* Volume is persistent across builds
* Logs may be used to generate a data-driven FAQ in the future

---

## 📌 Roadmap

* [x] RAG with LangChain + OpenAI
* [x] Automated deployment with GitHub Actions
* [x] Persistent interaction logging
* [ ] Implement caching for frequently asked questions and repeated answers.
* [ ] Auto-generated FAQ module
* [ ] Admin dashboard with usage metrics

---

## Testing & Security

* `bandit` for security scanning at build time
* `ruff` and `mypy` for linting and static typing
* CI pipeline fails on security violations

---
