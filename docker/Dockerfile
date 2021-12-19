FROM python:3.9.7-slim-bullseye

WORKDIR /usr/src/app
COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uwsgi

COPY ../ /usr/src/app
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV DEBUG=false

EXPOSE 5000

CMD ["uwsgi", "app.ini"]