FROM python:3.11

COPY ./app /reminder_backend/app
COPY requirements.txt manage.py /reminder_backend/

WORKDIR /reminder_backend/

RUN pip install -r requirements.txt

CMD python -u manage.py migrate && python manage.py runserver 0.0.0.0:8000
