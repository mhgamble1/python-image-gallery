#!/bin/bash

export IMAGE_GALLERY_SCRIPT_VERSION="1.1"

CONFIG_BUCKET="edu.au.cc.image-gallery-config-mg"

# Install packages
yum -y update
yum install -y python3 pip git nginx postgresql15 postgresql-devel gcc python3-devel

# Configure/install custom software
cd /home/ec2-user
git clone https://github.com/mhgamble1/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
su ec2-user -l -c "cd ~/python-image-gallery && pip install -r requirements.txt --user"

aws s3 cp s3://${CONFIG_BUCKET}/nginx/nginx.conf /etc/nginx
aws s3 cp s3://${CONFIG_BUCKET}/nginx/default.d/image_gallery.conf /etc/nginx/default.d

# Start/enable services
systemctl start nginx
systemctl enable nginx

su ec2-user -l -c "cd ~/python-image-gallery && ./start" >/var/log/image_gallery.log 2>&1 &
