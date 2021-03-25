FROM python:3.8

RUN apt-get install curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

WORKDIR /app

COPY . .

RUN $HOME/.poetry/bin/poetry install

CMD $HOME/.poetry/bin/poetry run python bin/script.py
