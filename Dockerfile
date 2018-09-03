FROM python:2.7-alpine

RUN adduser -D pomni

WORKDIR /home/pomni

COPY requirements.txt requirements.txt
RUN pip install virtualenv==15.1.0
RUN python -m virtualenv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY pomni.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP pomni.py

RUN chown -R pomni:pomni ./
USER pomni

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
