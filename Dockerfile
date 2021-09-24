# Dockerfile, Image, Container
FROM python:3.9

WORKDIR /hus-backend

COPY /backend/requirements.txt .

RUN pip install -r requirements.txt

COPY ./backend ./backend

EXPOSE 8000

CMD ["python", "./backend/main.py"]


#ADD backend/main.py .

#RUN pip install fastapi uvicorn


