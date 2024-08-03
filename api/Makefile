setup: clear
	python3 -m venv venv
	(. venv/bin/activate)
	pip install -r requirements.txt

clear:
	rm -rf venv

run:
	(. venv/bin/activate)
	FLASK_APP=index.py FLASK_ENV=development flask run