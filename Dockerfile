FROM tiangolo/uwsgi-nginx-flask:python3.7
#RUN apk --update add bash nano
ENV UWSGI_INI /app/uwsgi.ini
COPY . /app
RUN pip install -r /app/requirements.txt
