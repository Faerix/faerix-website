#proxy:="--proxy=129.104.242.2:8080"

.PHONY: depends install runserver 

venv:
	virtualenv --python=python3 venv

depends: venv requirements.txt
	. venv/bin/activate; \
	pip3 install -r requirements.txt $(proxy)

install: depends conv/migrations
	. venv/bin/activate; \
	python3 manage.py collectstatic --noinput; \
	python3 manage.py migrate

runserver: install
	. venv/bin/activate; \
	    python3 manage.py runserver 0.0.0.0:8080



