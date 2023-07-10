FROM python:3

WORKDIR /app



RUN pip3 install Flask  requests

COPY ./src ./src

ENV PORT = 13800

ENV FORWARDING_ADDRESS=''

EXPOSE 13800

CMD [ "python", "./src/index.py"]

