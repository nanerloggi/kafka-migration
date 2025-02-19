#! /usr/bin/env python3

import os
import json

import networkx as nx

from models.schema import Schema
from registry import Registry


SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL")
SCHEMA_REGISTRY_USERNAME = os.getenv("SCHEMA_REGISTRY_USERNAME", "")
SCHEMA_REGISTRY_PASSWORD = os.getenv("SCHEMA_REGISTRY_PASSWORD", "")


schemas = (
    Schema
        .select('subject', 'version')
        .select_raw('schema -> "references" as "references"')
        .get()
)

graph = nx.DiGraph()

for schema in schemas:
    node = (schema.subject, schema.version)
    graph.add_node(node)

    if schema.references is not None:
        for reference in json.loads(schema.references):
            graph.add_edge((reference.get("subject"), reference.get("version")), node)


sorted_schemas = list(nx.topological_sort(graph))


sr = Registry(SCHEMA_REGISTRY_URL, SCHEMA_REGISTRY_USERNAME, SCHEMA_REGISTRY_PASSWORD)

sr.set_global_import_mode()


for index, (subject, version) in enumerate(sorted_schemas):
    print(f"Creating {subject} v{version}")

    record = Schema.where("subject", subject).where("version", version).first()
    response, status_code = sr.create(record.subject, json.loads(record.schema))


# for subject, _ in sorted_schemas:
#     sr.set_readwrite_mode_on_subject(subject)
