FROM python:3.8
ENV PYTHONUNBUFFERED=1
#ARG APP_USER=appuser
#RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}
RUN mkdir /django/
RUN mkdir /AI/
WORKDIR /django/
# ADD src /django
RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    default-libmysqlclient-dev \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get install -y cron && touch /var/log/cron.log
#use python3
RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip



# COPY /src/backend/requirements.txt /code/
COPY /src/backend/manage.py /django/
COPY /src/backend /django/

RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    make \
    gcc \
    libpcre3-dev \
    libpq-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && python -m pip install --upgrade pip\
    && pip install --no-cache-dir -r requirements.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Add any static environment variables needed by Django or your settings file here:
# uWSGI will listen on this port
EXPOSE 8000
# Add any static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=core.settings

#FROM tensorflow/tensorflow:latest
#ENV CUDA_VISIBLE_DEVICES=-1
ENV TF_ENABLE_ONEDNN_OPTS=0
