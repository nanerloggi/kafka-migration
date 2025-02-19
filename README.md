# Kafka Migration

## Requirements
- Python >= 3.11
- Poetry
- Make
- SQLite3

## Installation
```bash
pyenv install $(cat .python-version)
poetry config virtualenvs.in-project true
poetry install
```

## Migrating Schema Registry

#### Exporting Schemas
```shell
make migrate
SCHEMA_REGISTRY_URL=http://your-source-registry:8081 ./01-dump-registry.py
```

#### Migrating Schemas
```shell
SCHEMA_REGISTRY_URL=http://your-target-registry:8081 ./02-migrate-to.py
```

#### Environment Variables

| Name                       | Description              |
| ---------------------------| ------------------------ |
| `SCHEMA_REGISTRY_URL`      | Registry URL             |
| `SCHEMA_REGISTRY_USERNAME` | Basic HTTP Auth Username |
| `SCHEMA_REGISTRY_PASSWORD` | Basic HTTP Auth Password |