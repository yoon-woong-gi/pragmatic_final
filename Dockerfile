FROM python:3.9.0

WORKDIR /home/

RUN echo "testing"

RUN git clone https://github.com/junnman0216/pragmatic.git

WORKDIR /home/pragmatic/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

RUN echo "SECRET_KEY=django-insecure-1^5r-wn&ffhit&e@cjbwgt#3z71b3fvtrlw#g9%h07a4$%hmet" > .env

RUN python manage.py collectstatic

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate --settings=pragmatic.settings.deploy && gunicorn pragmatic.wsgi --env DJANGO_SETTINGS_MODULE=pragmatic.settings.deploy --bind 0.0.0.0:8000"]

