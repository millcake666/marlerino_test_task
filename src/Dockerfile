FROM python:3.10-alpine
ENV TZ='Asia/Yekaterinburg'

WORKDIR /api/

COPY requirements.txt ./requirements.txt

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install --no-cache-dir --upgrade -r requirements.txt


COPY ./src/ ./
COPY ../.env ./
EXPOSE 8000

CMD ["python", "main.py"]
