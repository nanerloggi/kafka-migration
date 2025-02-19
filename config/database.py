from masoniteorm.connections import ConnectionResolver


DATABASES = {
  "default": "sqlite",
  "sqlite": {
    "driver": "sqlite",
    "database": "schemas.db",
  }
}

DB = ConnectionResolver().set_connection_details(DATABASES)
