FROM python:3.11-slim

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    DOCKERIZE_VERSION=v0.6.1

# Установка всіх потрібних бібліотек
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python3-tk \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Робоча директорія для установки залежностей
WORKDIR /pysetup

COPY ./drf_warehouse/requirements.txt .

# Додатково ставимо wheel, бо Pillow цього часто вимагає
RUN pip install --upgrade pip && pip install wheel && pip install -r requirements.txt

# Встановлюємо dockerize
RUN wget "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && tar -C /usr/local/bin -xzvf "dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && rm "dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz"

# Копіюємо запускні скрипти
COPY ./docker/api_warehouse/docker-entrypoint.sh ./docker/api_warehouse/wait-for-command.sh ./docker/api_warehouse/runserver.sh /
RUN chmod +x /docker-entrypoint.sh /wait-for-command.sh /runserver.sh

# Робоча директорія з кодом
WORKDIR /code

ENTRYPOINT ["/docker-entrypoint.sh"]