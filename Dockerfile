FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update && apt-get -y install cron

# SETUP UWSGI
ENV UWSGI_INI /app/uwsgi.ini

# COPY REQUIREMENTS (Do this first to save computation & memory bandwidth over the layers)
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# COPY APP
COPY . /app

# Setup cron job
#COPY data_fetch_cron /etc/cron.d/data_fetch_cron
#RUN chmod 0644 /etc/cron.d/data_fetch_cron
#RUN crontab /etc/cron.d/data_fetch_cron
#RUN touch /var/log/cron.log
#RUN cron



