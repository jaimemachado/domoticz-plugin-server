
FROM python:3.6-slim-stretch
MAINTAINER Jaime Machado
RUN apt-get update -y
RUN apt-get install -y python3 python-pip-whl python3-pip build-essential libssl-dev libffi-dev python-dev
COPY /app /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 8050
ENTRYPOINT ["python3"]
CMD ["main.py"]
