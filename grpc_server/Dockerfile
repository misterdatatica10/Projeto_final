# Use uma imagem base leve do Python
FROM python:3.10-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o container
COPY . .

# Exponha a porta onde o servidor gRPC estará escutando
EXPOSE 50051

# Comando para iniciar o servidor gRPC
CMD ["python", "main.py"]