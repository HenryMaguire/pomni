FROM python:3.6-alpine

RUN adduser -D pomni

WORKDIR /home/pomni


COPY requirements.txt requirements.txt
RUN pip3 install virtualenv==15.1.0
RUN python3 -m virtualenv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql==0.7.2

RUN export FLASK_ENV=development
RUN export FLASK_DEBUG=False

COPY app app
COPY migrations migrations
COPY pomni.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP pomni.py

RUN chown -R pomni:pomni ./
USER pomni

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
