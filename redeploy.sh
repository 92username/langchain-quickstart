#!/usr/bin/env bash

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

# Verificar e instalar python3-venv se necessário
echo "🔍 Verificando requisitos do sistema..."
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
VENV_PACKAGE="python3-venv"

if ! dpkg -l | grep -q "$VENV_PACKAGE"; then
  echo "📦 Instalando $VENV_PACKAGE (necessário para ambientes virtuais)..."
  sudo apt update
  sudo apt install -y $VENV_PACKAGE
fi

# Se estamos usando Python 3.12 especificamente, instale o pacote específico
if python3 --version | grep -q "3.12"; then
  if ! dpkg -l | grep -q "python3.12-venv"; then
    echo "📦 Instalando python3.12-venv..."
    sudo apt update
    sudo apt install -y python3.12-venv
  fi
fi

# Configurar ambiente virtual
echo "🛠️ Configurando ambiente virtual..."
if [ ! -d ".venv" ]; then
  # Remover qualquer .venv parcial ou corrompido
  rm -rf .venv
  python3 -m venv .venv
fi
source .venv/bin/activate

# Instalar/atualizar dependências
echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

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