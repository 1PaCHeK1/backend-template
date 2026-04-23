import aioinject

from app.storages.db.base.engine import (
    create_engine,
    create_session_factory,
    get_session,
)
from app.storages.db.settings import DatabaseSettings
from app.storages.db.uow import UnitOfWork
from lib.di import Providers, SettingsProvider

providers: Providers = [
    SettingsProvider(DatabaseSettings),
    aioinject.Singleton(create_engine),
    aioinject.Singleton(create_session_factory),
    aioinject.Scoped(get_session),
    aioinject.Scoped(UnitOfWork),
]
