FROM tiangolo/meinheld-gunicorn-flask:python3.7

ENV PYTHONUNBUFFERED 1
ENV STATIC_URL /static
ENV STATIC_PATH /app/app/static

WORKDIR /app

COPY src/prestart.sh /app

COPY src/requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
COPY src/app /app/app
COPY src/main.py /app
