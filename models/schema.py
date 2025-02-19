from masoniteorm import Model


class Schema(Model):
    __fillable__ = ["subject", "schema_id", "version", "schema"]
