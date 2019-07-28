FROM ubuntu:latest
MAINTAINER Thijs Jeffrey "jeffrey.thijs@hotmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential sqlite3 libsqlite3-dev
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["pft.py"]