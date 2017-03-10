"""
Init todo list values
"""

from yoyo import step

__depends__ = {'20170310_01_O749B-init-db'}

steps = [
    step("""
    INSERT INTO todo ("name") VALUES ('Hi, it''s your first job =)'), ('Everything else')
    """)
]
