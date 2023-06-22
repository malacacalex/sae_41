FROM debian:11

RUN apt update && apt upgrade -y
RUN apt install -y python3-pip default-libmysqlclient-dev
RUN pip install flask flask-mysqldb

CMD mkdir templates
COPY templates/* templates/
COPY app.py app.py
CMD flask --app app.py run
