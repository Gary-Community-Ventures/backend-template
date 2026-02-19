.PHONY: install run dev lint format test clean

install:
	pip install -r requirements.txt

run:
	python run.py

dev:
	python run.py

prod:
	gunicorn wsgi:app

lint:
	flake8 app/

format:
	black app/

test:
	pytest

test-cov:
	pytest --cov=app

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
