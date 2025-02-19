"""CreateSchemasTable Migration."""

from masoniteorm.migrations import Migration


class CreateSchemasTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("schemas") as table:
            table.increments("id")
            table.timestamps()

            table.string("subject")
            table.integer("schema_id")
            table.integer("version")
            table.text("schema")
            table.unique(["subject", "schema_id", "version"])


    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("schemas")
