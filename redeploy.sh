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

echo "Atualizando repositório..."
cd ~/langchain-quickstart
git pull origin main

echo "Parando container atual..."
docker compose down

echo "Rebuildando imagem do zero..."
docker compose build --no-cache

echo "Subindo container atualizado..."
docker compose up -d

echo "Deploy completo."
