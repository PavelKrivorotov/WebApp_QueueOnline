# syntax=docker/dockerfile:1

FROM python:3.10-alpine3.15
WORKDIR /app/

# Add and install requirements.txt
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Add .env variables
ADD ./.docker.env /app/.env

# Add script-files
ADD ./src /app/src

ENTRYPOINT [ "python",  "src/main.py" ]
