FROM python:3.13-slim

WORKDIR /

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
