FROM ubuntu:latest

# Set the environment variable
ENV DEBIAN_FRONTEND=noninteractive

# Set the timezone
RUN echo "America/Chicago" > /etc/timezone && \
    apt-get update -y && apt-get install -y tzdata apt-utils && \
    ln -fs /usr/share/zoneinfo/America/Chicago /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    apt-get install -y python3 python3-pip python3-venv git postgresql gcc libpq-dev

COPY . .
run pip3 install -r requirements.txt

EXPOSE 5555

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
CMD ["uwsgi", "--http", "5555", "--module", "app:app"]

