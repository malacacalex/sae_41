FROM debian:11

RUN apt update && apt upgrade -y
RUN apt install -y python3-pip default-libmysqlclient-dev
RUN pip install flask flask-mysqldb

# Installation de MySQL
RUN apt-get install -y mysql-server

# Copie du fichier de base de données
COPY db.db /var/lib/mysql/db.db

CMD mkdir templates
COPY templates/* templates/
COPY app.py app.py

# Exécution de MySQL et de l'application Flask
CMD service mysql start && flask --app app.py run --host=0.0.0.0
