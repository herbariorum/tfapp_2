from peewee import Model, PostgresqlDatabase

db = PostgresqlDatabase(
    "cepada_api",
    user="postgres",
    password="Elias2024",
    host="localhost",
    port=5432,
    )


class BaseModel(Model):
    class Meta:
        database = db
