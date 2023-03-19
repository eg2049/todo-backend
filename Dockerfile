# получение образа python
FROM python:3.9

# создание рабочей директории в контейнере
RUN mkdir /app

# установка рабочей директории в контейнере
WORKDIR /app

# добавление проекта в рабочую директорию контейнера
ADD . /app/

# установка переменных окружения в контейнере
# также переменную можно передать в команде запуска -e TZ=Europe/Moscow
ENV TZ Europe/Moscow
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

ENV VENV=/app/venv
ENV VENV_ACTIVATE="$VENV/bin/activate"

# установка утилит для работы
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    python3-setuptools \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# создание виртуального окружения python
RUN python3 -m venv $VENV

# активация вирутального окружения / установка зависимостей проекта
RUN . $VENV_ACTIVATE && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# другой вариант
# RUN . $VENV_ACTIVATE && pip install pipenv
# RUN . $VENV_ACTIVATE && pipenv install --skip-lock --system --dev

# декларация что этот порт можно пробросить наружу 
# при запуске контейнера, указать параметр -p порт_локальной_машины:порт_в_контейнере
# EXPOSE 8888

# во время запуска -v абсолютный_путь_на_локальной_машине:абсолютный_путь_в_контейнере для монтирования директории на локальной машине к контейнеру
# во время запуска -v имя_volume:абсолютный_путь_в_контейнере для монтирования volume-а
# в этой директории можно к примеру изменять файлы которые нужны в контейнере и контейнер увидит эти изменения
# также контейнер сам может изменять локальные файлы в этой директории

# активация вирутального окружения получение / накатывание миграций / запуск приложения
CMD . $VENV_ACTIVATE && python3 manage.py migrate && python3 manage.py runserver $HOST:$PORT --noreload

# другой вариант
# CMD gunicorn todo_backend.wsgi:application --bind $HOST:$PORT
