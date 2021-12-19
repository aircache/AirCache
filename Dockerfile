FROM python:3.10-slim as build
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
	build-essential gcc 

WORKDIR /usr/app
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

FROM python:3.10-slim@sha256:2bac43769ace90ebd3ad83e5392295e25dfc58e58543d3ab326c3330b505283d
RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python
RUN mkdir /usr/app && chown python:python /usr/app
WORKDIR /usr/app
COPY --chown=python:python --from=build /usr/app/venv ./venv
COPY --chown=python:python . .
USER 999

ENV PORT="5000"
ENV HOST="http://127.0.0.1:5000"
ENV FLASK_APP="run.py"
ENV FLASK_ENV="production"
ENV DEBUG="false"
ENV STORAGE_OPTION="file"
ENV CACHE_OPTION="memory"
ENV EXP_CONF="10"
ENV PATH="/usr/app/venv/bin:$PATH"

EXPOSE 5000

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "run:app" ]