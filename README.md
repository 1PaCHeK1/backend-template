# Main Structure
```
src/
    alembic/
        ...
    app/
        adapters/
            ...
        connectors/
            ...
        core/
            di/
            domain/
                ...
                shared/
        storages/
            ...
        telemetry/
            ...
    lib/
        ...
tests/
    factories/
        ...
    plugins/
        ...
```

## Legend

```
src.app.adapters - driving ports that affect the application
```

```
src.app.connectors - driven ports affecting third-party apps
```

```
src.app.core - the main app that encapsulates all of the application's business and data management logic

src.app.core.di - IoC container

src.app.core.domain - domain logic modules

src.app.core.domain.shared - shared domain logic modules

Domains don't depends on src.app.adapters and other domains, except the shared ones
```

```
src.app.storages - storages (postgresql, s3, etc.)
```

```
src.app.telemetry - integration with logging and monitoring services (sentry, elk, etc.)
```

```
src.lib - generic utils
```
