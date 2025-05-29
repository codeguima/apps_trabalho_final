FROM python:3.9-slim

# Instala dependências do sistema (úteis para pacotes como mysql-connector-python)
RUN apt-get update && apt-get install -y gcc libmariadb-dev && apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variáveis de ambiente
ENV FLASK_APP=app:create_app
ENV FLASK_ENV=development

# Exponha a porta (boa prática)
EXPOSE 5000

# Comando para iniciar o Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
