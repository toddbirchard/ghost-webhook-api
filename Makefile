SRCPATH := $(CURDIR)
ENTRYPOINT := $(shell find $(SRCPATH) -name '*.ini')
PROJECTNAME := $(shell basename "$PWD")

define HELP
Manage $(PROJECTNAME).

Usage:

make run	      - Run uWSGI server for $(PROJECTNAME).
make restart	  - Purge cache & reinstall modules.
make deploy	    - Pull latest build and deploy to production.
make update	    - Update all pip dependencies in both poetry and pipenv environments.
make clean	    - Remove cached files.
endef
export HELP


.PHONY: run restart update help


all help:
	@echo "$$HELP"


.PHONY: run
run:
	nohup uwsgi $(ENTRYPOINT) &


.PHONY: restart
restart:
	pkill -9 -f $(shell uwsgi $(ENTRYPOINT))
	nohup uwsgi $(ENTRYPOINT) &


.PHONY: deploy
deploy:
	$(shell git pull origin master)
	$(shell pkill -9 -f  "uwsgi $(ENTRYPOINT)"))
	$(shell pipenv update)
	service api restart
	
	
.PHONY: update
update:
	poetry shell
	poetry update
	$(shell exit)
	pipenv shell
	pipenv update
	pip3 freeze > requirements.txt
	
	
.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete