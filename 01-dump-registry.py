#! /usr/bin/env python3

import os
import json

from models.schema import Schema
from registry import Registry


SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL")
SCHEMA_REGISTRY_USERNAME = os.getenv("SCHEMA_REGISTRY_USERNAME")
SCHEMA_REGISTRY_PASSWORD = os.getenv("SCHEMA_REGISTRY_PASSWORD")


sr = Registry(SCHEMA_REGISTRY_URL, SCHEMA_REGISTRY_USERNAME, SCHEMA_REGISTRY_PASSWORD)

for subject in sr.subjects():
    for version in sr.versions(subject):
        print(f"Dumping {subject} v{version}")

        schema = sr.version(subject, version)

        record = {
            "schema_id": schema.get("id"),
            "subject": subject,
            "version": version,
            "schema": json.dumps(schema),
        }

        Schema.first_or_create(record, record)
