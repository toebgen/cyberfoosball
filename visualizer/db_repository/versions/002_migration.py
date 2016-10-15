from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
game = Table('game', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('timestamp', DateTime),
    Column('body', String(length=140)),
    Column('home_defense', Integer),
    Column('home_offense', Integer),
    Column('guest_defense', Integer),
    Column('guest_offense', Integer),
    Column('home_goals', Integer),
    Column('guest_goals', Integer),
)

games = Table('games', post_meta,
    Column('game_id', Integer),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['game'].create()
    post_meta.tables['games'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['game'].drop()
    post_meta.tables['games'].drop()
