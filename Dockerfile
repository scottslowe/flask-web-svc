FROM python:alpine

MAINTAINER Scott S. Lowe <scott.lowe@scottlowe.org>
LABEL maintainer="Scott S. Lowe <scott.lowe@scottlowe.org>"

ARG GIT_COMMIT=unspecified
LABEL git_commit=$GIT_COMMIT

RUN pip install flask

COPY app /app/

EXPOSE 5000

ENTRYPOINT ["python", "/app/main.py"]
