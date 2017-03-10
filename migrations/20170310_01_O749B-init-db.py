"""
Init db
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE "public".todo(
            "id" bigserial NOT NULL,
            "name" text NOT NULL,
            "creation_time" timestamp NOT NULL DEFAULT NOW(),
            PRIMARY KEY ("id")
        )
        WITH (OIDS=FALSE);
        """
    )
]
