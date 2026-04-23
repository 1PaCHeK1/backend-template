import aioinject

from app.storages.db.base.engine import (
    create_engine,
    create_session_factory,
    get_session,
)
from app.storages.db.settings import DatabaseSettings
from app.storages.db.uow import UnitOfWork
from lib.di import Providers, register_settings

providers: Providers = [
    register_settings(DatabaseSettings),
    aioinject.Singleton(create_engine),
    aioinject.Singleton(create_session_factory),
    aioinject.Scoped(get_session),
    aioinject.Scoped(UnitOfWork),
]
