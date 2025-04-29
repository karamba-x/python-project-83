install:
	uv sync

build:
	./build.sh

dev:
	uv run flask --debug --app page_analyzer:app run

lint:
	uv run ruff check page_analyzer --fix

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer:app

render-start:
	gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer:app
