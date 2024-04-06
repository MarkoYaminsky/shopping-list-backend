FROM python:3.11

COPY ./app /shopping_list_backend/app
COPY requirements.txt manage.py /shopping_list_backend/

WORKDIR /shopping_list_backend/

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
