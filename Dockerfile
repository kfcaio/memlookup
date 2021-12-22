FROM python:3.9-slim-bullseye

WORKDIR /usr/src/app

RUN apt-get update

COPY requirements.txt requirements.txt
COPY main.py main.py
COPY volatile.py volatile.py

RUN pip install -r requirements.txt
RUN mkdir -p /tmp/regs
ENV SERVER_DATA_DIR=/tmp/regs

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
