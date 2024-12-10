FROM python:3.10

USER root

RUN apt-get update \
    && apt-get install -y python3.10 pip \
    && apt-get install -y libgl1-mesa-dev \
    && pip install --upgrade pip \
    && pip install --upgrade setuptools

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/app

COPY ./app /root/app
COPY ./requirements.txt /root/app/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8080
EXPOSE 5000

# Flaskが動的にPORT環境変数を使用するようにCMDを修正
CMD ["sh", "-c", "flask run -h 0.0.0.0 -p $PORT"]