SRCPATH := $(shell pwd)
PROJECTNAME := $(shell basename $(CURDIR))
ENTRYPOINT := $(PROJECTNAME).ini

define HELP
Manage $(PROJECTNAME). Usage:

make run        - Run $(PROJECTNAME).
make restart    - Purge cache & reinstall modules.
make deploy     - Pull latest build and deploy to production.
make update     - Update pip dependencies in both poetry and pipenv environments.
make clean      - Remove cached files and lock files.
endef
export HELP


.PHONY: run restart deploy update clean help


all help:
	@echo "$$HELP"


.PHONY: run
run:
	service $(PROJECTNAME) start


.PHONY: restart
restart:
	service $(PROJECTNAME) stop
	make clean
	service $(PROJECTNAME) start
	service $(PROJECTNAME) status


.PHONY: deploy
deploy:
	service $(PROJECTNAME) stop
	git stash
	git pull origin master
	# $(shell source ./dependencies.sh)
	service $(PROJECTNAME) start
	service $(PROJECTNAME) status


.PHONY: update
update:
	poetry update
	poetry shell
    $(shell pip3 freeze > requirements.txt)
	# $(shell source ./dependencies.sh)


.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name 'poetry.lock' -delete
	find . -name 'Pipefile.lock' -delete