FROM scratch
ENTRYPOINT ["/run_app"]
USER 65535
COPY --chown=65535:65535 tmp /tmp
COPY --chown=65535:65535 conf /conf
COPY --chown=65535:65535 run_app /

ENV PORT="5000"
ENV HOST="http://127.0.0.1:5000"
ENV FLASK_APP="run.py"
ENV FLASK_ENV="production"
ENV DEBUG="true"
ENV STORAGE_OPTION="file"
ENV CACHE_OPTION="memory"
ENV EXP_CONF="10"
ENV TEST_ENV="Environment variables are identified"

EXPOSE 5000

