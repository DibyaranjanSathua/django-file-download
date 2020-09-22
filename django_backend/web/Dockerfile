FROM python:3.7-slim

ARG APP_NAME=backend
ARG APP_HOME=/usr/src/app
ARG STATIC_FILE=staticfiles
ARG MEDIA_FILE=mediafiles
ARG ROI_FILE=roifiles

WORKDIR ${APP_HOME}/${APP_NAME}

# Create a group and user to run our app
ARG APP_USER=sathua
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential gcc python3-dev python3-venv \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ${APP_HOME}/requirements.txt

ENV VENV ${APP_HOME}/venv
RUN python3 -m venv $VENV
ENV PATH "$VENV/bin:$PATH"

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r ${APP_HOME}/requirements.txt

EXPOSE 8000

# Copy project
COPY ./${APP_NAME} ${APP_HOME}/${APP_NAME}

# Create staticfiles and media file directory
RUN mkdir -p ${APP_HOME}/${APP_NAME}/${STATIC_FILE} ${APP_HOME}/${APP_NAME}/${MEDIA_FILE} ${APP_HOME}/${APP_NAME}/${ROI_FILE}

# After evrything get copied and the ownership to APP_USER.
# Even if we change the USER, COPY and ADD with copy the files to docker image as root,
# Docker image should run as non-root user
RUN chown -R ${APP_USER}:${APP_USER} ${APP_HOME}
USER ${APP_USER}
