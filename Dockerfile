FROM python:3.10.13-slim-bullseye
WORKDIR /app
COPY /app /app
RUN apt update && apt install wget -y
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install ./google-chrome-stable_current_amd64.deb -y
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["-u", "serve.py"]
