
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ADD . /srv
WORKDIR /srv
ADD ./requirements.txt /srv/requirements.txt
RUN pip install -r requirements.txt
COPY ./app /app