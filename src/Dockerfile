FROM python:3.14-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y netcat-traditional make curl \
  && pip install --default-timeout=100 poetry

COPY ./pyproject.toml ./poetry.lock ./

ARG DEV_DEPS=False

RUN poetry config virtualenvs.create false
RUN if [ $DEV_DEPS = True ] ; then \
  poetry install --no-root --no-interaction --no-ansi ; else \
  poetry install --no-root --only main --no-interaction --no-ansi ; fi

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .

WORKDIR /usr/src/app/src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]