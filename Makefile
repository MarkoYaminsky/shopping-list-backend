runserver:
	docker exec -it reminder-backend python manage.py runserver

install-requirements:
	docker exec -it reminder-backend pip install -r requirements.txt

launch-docker:
	bash docker-launch.sh

launch-docker-build:
	bash docker-launch.sh build
