install:
	pip install -r requirements.txt

dev:
	flask --debug --app page_analyzer:app run

start:
	gunicorn -w 4 -b 0.0.0.0:8000 page_analyzer:app

lint:
	ruff check page_analyzer --fix