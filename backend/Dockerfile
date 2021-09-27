# Dockerfile, Image, Container
FROM python:3.9

WORKDIR /hus

COPY /app/requirements.txt .

RUN pip install -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["python", "./app/main.py"]


#ADD app/main.py .

#RUN pip install fastapi uvicorn


