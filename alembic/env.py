from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

from app.db.models import Base
from config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', settings.database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


def set_role(context):
    db_owner = settings.database_role
    if db_owner:
        sql = f'set role {db_owner}'
        context.execute(sql)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        set_role(context)
        context.run_migrations()


def run_migrations_online():
    # Pool size and max_overflow can be tweaked depending on memory and
    # database settings. Connection time-out is fixed at 1 second.
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        pool_size=10,
        max_overflow=20,
        pool_timeout=1,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True  # Required for SQLite and certain type of migrations in other DBs
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
