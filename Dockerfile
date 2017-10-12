FROM python:alpine

MAINTAINER Scott S. Lowe <scott.lowe@scottlowe.org>

RUN pip install flask

COPY app /app/

EXPOSE 5000

ENTRYPOINT ["python", "/app/main.py"]
