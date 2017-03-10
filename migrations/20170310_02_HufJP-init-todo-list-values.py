"""
Init todo list values
"""

from yoyo import step

__depends__ = {'20170310_01_O749B-init-db'}

steps = [
    step("""
    INSERT INTO todo ("name", "creation_time") VALUES
        ('Hi, it''s your first job =)', '2016-01-01 12:13:01'),
        ('Everything else', '2016-02-01 12:13:01')
    """)
]
