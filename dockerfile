FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash appuser


COPY --chown=appuser:appuser requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY --chown=appuser:appuser . /app/


COPY entrypoint.sh /entrypoint.sh


RUN chmod +x /entrypoint.sh

USER appuser

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "bs23apiproject.wsgi:application", "--bind", "0.0.0.0:8000"]

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}
