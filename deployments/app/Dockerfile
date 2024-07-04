FROM python:3.11.4

ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq && apt-get install -y \
    # std libs
    git curl vim wget bash-completion gettext \
    # geodjango
    gdal-bin binutils libproj-dev libgdal-dev \
    # postgresql
    libpq-dev postgresql-client \
    # daphne 
    #daphne \
    # cron
    cron \
    # redis
    # redis-tools \
    && apt-get clean && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/* \
    && addgroup --system gustabo \
    && adduser --system --ingroup gustabo gustabo

RUN pip install nltk
RUN ["python", "-m", "nltk.downloader", "punkt"] 
RUN pip install boto3
WORKDIR /app

# Requirements are installed here to ensure they will be cached.
COPY ./deployments/app/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY --chown=gustabo:gustabo ./deployments/app/cmds/* /cmds/
RUN sed -i 's/\r$//g' /cmds/* \
    && chmod -R +x /cmds \
    && mkdir -p /var/log/ \
    && chown -R gustabo /cmds /var/log/

COPY --chown=gustabo:gustabo . .

USER root
