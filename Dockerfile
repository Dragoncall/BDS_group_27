FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update && apt-get -y install cron

# Install python and hosting. Also copy app
ENV UWSGI_INI /app/uwsgi.ini
COPY . /app
RUN pip install -r /app/requirements.txt

# Setup cron job
COPY data_fetch_cron /etc/cron.d/data_fetch_cron
RUN chmod 0644 /etc/cron.d/data_fetch_cron
RUN crontab /etc/cron.d/data_fetch_cron
RUN touch /var/log/cron.log
RUN cron



