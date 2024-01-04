FROM python:3.11

COPY ./app /opt/app
COPY requirements.txt manage.py /opt/

WORKDIR /opt/

RUN pip install -r requirements.txt

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
