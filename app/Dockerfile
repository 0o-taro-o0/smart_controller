FROM python:3.11

WORKDIR /app
ENV FLASK_APP=app

COPY ./smart_controller_app/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
