FROM python:latest as build
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
	build-essential gcc 

RUN pip install pyinstaller 
RUN apt install binutils wget -y
RUN cd / && wget https://github.com/NixOS/patchelf/archive/0.10.tar.gz
RUN tar xzf 0.10.tar.gz
RUN cd patchelf-0.10/ && ./bootstrap.sh && ./configure && make && make install
RUN pip install staticx

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install waitress

COPY . .

RUN pyinstaller -F run.py && cd dist && staticx run run_app

FROM scratch
ENTRYPOINT ["/run_app"]
USER 65535
COPY --chown=65535:65535 --from=build ./app/dist/run_app /
COPY --chown=65535:65535 --from=build ./app/conf /conf
COPY --chown=65535:65535 --from=build ./app/tmp /tmp

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

