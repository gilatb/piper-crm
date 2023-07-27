FROM python:3.11.4-slim

RUN apt-get update && apt-get install -y make

RUN python -m venv venv
RUN . /venv/bin/activate && pip install --upgrade pip

WORKDIR /code

COPY Makefile requirements.txt .

RUN make requirements

ADD . /

CMD ["make", "start"]
