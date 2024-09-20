# Usando a imagem base com Python 3.10
FROM python:3.10-slim

# Copia tudo no diretório atual para o /app no container
COPY . /app

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências listadas no requirements.txt
RUN pip install -r requirements.txt

# Expõe as portas do Streamlit e FastAPI
EXPOSE 8501
EXPOSE 8000

# Cria o diretório de configuração do Streamlit
RUN mkdir ~/.streamlit

# Copia as configurações do Streamlit para o diretório correto
COPY .streamlit /root/.streamlit

# Define o comando para rodar FastAPI e Streamlit
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port=8501 --server.address=0.0.0.0"]
