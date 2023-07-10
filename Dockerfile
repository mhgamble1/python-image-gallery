FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Fix timezone for tzdata installation so it doesn't prompt for input
RUN echo "America/Chicago" > /etc/timezone && \
    apt-get update -y && apt-get install -y tzdata apt-utils && \
    ln -fs /usr/share/zoneinfo/America/Chicago /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    apt-get install -y python3 python3-pip git postgresql gcc libpq-dev

COPY . .

ENV PG_HOST=host.docker.internal \
    PG_PORT=5432 \
    IG_DATABASE=image_gallery \
    IG_USER=image_gallery \
    S3_IMAGE_BUCKET=edu.au.cc.image-gallery \
    AWS_ACCESS_KEY_ID_FILE=/aws_access_key_id \
    AWS_SECRET_ACCESS_KEY_FILE=/aws_secret_access_key

RUN pip3 install -r requirements.txt

EXPOSE 5555

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
RUN chmod +x /start.sh
CMD ["/start.sh", "uwsgi", "--http", ":5555", "--module", "gallery.ui.app:app"]
