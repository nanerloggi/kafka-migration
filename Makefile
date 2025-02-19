.PHONY: test

ORMCMD := $(shell which masonite-orm)
SQLITE := $(shell which sqlite3)


clean:
	@rm -rf schemas.db

migrate:
	@$(ORMCMD) migrate --directory db/migrations

dbconsole:
	@$(SQLITE) -header -column schemas.db
