# from __future__ import print_function
# from logging.config import fileConfig

# from sqlalchemy import create_engine, pool
# from alembic import context
# from play_music_track.models.base import Base  # Import the base
# from play_music_track.models.models import Audio  # Import your models

# # Alembic Config object
# config = context.config

# # Interpret the config file for Python logging
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# # Add your model's MetaData object here
# target_metadata = Base.metadata


# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode.

#     This configures the context with just a URL
#     and not an Engine, though an Engine is acceptable here as well.
#     """
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )

#     with context.begin_transaction():
#         context.run_migrations()


# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode.

#     This creates a synchronous connection engine and runs migrations online.
#     """
#     connectable = create_engine(
#         config.get_main_option("sqlalchemy.url"),
#         poolclass=pool.NullPool,
#     )

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection,
#             target_metadata=target_metadata,
#             compare_type=True,  # Compare column types
#             compare_server_default=True,  # Compare server defaults
#         )

#         with context.begin_transaction():
#             context.run_migrations()


# # Determine if the context is offline or online, and run the appropriate migration function
# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()


# --------------------- for asyncpf +postgress ----------------------------

# from __future__ import print_function
# from logging.config import fileConfig

# from sqlalchemy import pool
# from alembic import context
# from sqlalchemy.ext.asyncio import create_async_engine

# from play_music_track.models.base import Base  # Import the base
# from play_music_track.models.models import Audio  # Import your models


# # Alembic Config object
# config = context.config

# # Interpret the config file for Python logging
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# # Add your model's MetaData object here
# target_metadata = Base.metadata


# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode.

#     This configures the context with just a URL
#     and not an Engine, though an Engine is acceptable here as well.
#     """
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )

#     with context.begin_transaction():
#         context.run_migrations()


# async def run_migrations_online() -> None:
#     """Run migrations in 'online' mode.

#     This creates an async connection engine and runs migrations online.
#     """
#     connectable = create_async_engine(
#         config.get_main_option("sqlalchemy.url"),
#         poolclass=pool.NullPool,
#     )

#     async with connectable.connect() as connection:
#         await connection.run_sync(do_run_migrations)

#     await connectable.dispose()


# def do_run_migrations(connection):
#     """Configure the migration context to run migrations."""
#     context.configure(
#         connection=connection,
#         target_metadata=target_metadata,
#         compare_type=True,  # Compare column types
#         compare_server_default=True,  # Compare server defaults
#     )

#     with context.begin_transaction():
#         context.run_migrations()


# # Determine if the context is offline or online, and run the appropriate migration function
# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     import asyncio

#     asyncio.run(run_migrations_online())


# ---------------------------for psycopg3-------------------------------

import sys
import asyncio
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

config = context.config
fileConfig(config.config_file_name)

from play_music_track.models.base import Base
from play_music_track.models.models import Audio

target_metadata = Base.metadata


# The connection string must be synchronous for migrations
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
