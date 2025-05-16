#!/bin/bash

# redeploy manual script para atualizar o container do langchain-quickstart
# Este script deve ser executado na pasta ~/langchain-quickstart
# Certifique-se de que o script tenha permissão de execução:
# chmod +x redeploy.sh
# Para executar o script, use o seguinte comando:
# ./redeploy.sh
# Este script assume que o docker compose está instalado e configurado corretamente
# e que o repositório langchain-quickstart está clonado na pasta ~/langchain-quickstart
set -e

echo "🔄 Atualizando repositório..."
cd ~/langchain-quickstart
git pull origin main

echo "🧠 Executando pipeline RAG..."
python3 index_docs.py
python3 loader.py
python3 retriever.py

echo "🧼 Parando container atual..."
docker compose down

echo "🔧 Rebuild da imagem (no cache)..."
docker compose build --no-cache

echo "🚀 Subindo container atualizado..."
docker compose up -d

echo "✅ Deploy concluído com sucesso."
