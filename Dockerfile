# Container Build File for the webapp ( Flask - Gunicorn )

FROM tiangolo/meinheld-gunicorn-flask:latest


COPY ./requirements.txt /requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

COPY . /app

ENV MODULE_NAME="main"
ENV VARIABLE_NAME="app"
ENV PORT="80"

# TODO add args from
# https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2
# like SSL, Fallbacks ....

# documented at https://hub.docker.com/r/tiangolo/meinheld-gunicorn-flask

# ENV GUNICORN_CONF="/path/to/gunicorn_conf.py"

# default is 2 ( per cpu core )
ENV WORKERS_PER_CORE="3"

ENV MODE="aws"