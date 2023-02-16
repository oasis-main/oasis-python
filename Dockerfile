# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /client_app
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt 
COPY . .
#Streamlit runs on port 8501
EXPOSE 8501
CMD [ "streamlit",  "run", "streamlit_stripe_demo.py"]

#To run endpoint on, say, port 8500, execute:
# $ docker run --publish 8500:8501 oasis-markets-client