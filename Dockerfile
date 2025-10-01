FROM python:3.13-alpine
WORKDIR copy/
COPY . .
RUN pip install -r requirements.txt
