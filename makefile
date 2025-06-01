.PHONY: runserver

run:
	cd project && python manage.py runserver

subscribe:
	cd project && python manage.py subscribe