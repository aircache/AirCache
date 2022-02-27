
FROM ubuntu
RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python
RUN mkdir /usr/app && chown python:python /usr/app
WORKDIR /usr/app
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

EXPOSE 5000

CMD [ "./run" ]