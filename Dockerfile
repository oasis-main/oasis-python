# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /server_app
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt 
COPY . .
EXPOSE 8502
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8502", "--reload" ]


#To build, run:
#  $ docker build -t paddyc8/oasis-markets:api_v.[x.x] .
#  $ docker push paddyc8/oasis-markets:api_v.[x.x]
#To run locally on, say, port 8501, execute:
#  $ docker run --publish 8502:8501 oasis-markets-server