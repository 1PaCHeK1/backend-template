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
            domain/
                ...
                shared/
        di/
            ...
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

### Legend

```
src.app.adapters - driving ports that affect the application
```

```
src.app.connectors - driven ports affecting third-party apps
```

```
src.app.core - the main app that encapsulates all of the application's business and data management logic


src.app.core.domain - domain logic modules

src.app.core.domain.shared - shared domain logic modules

Domains don't depends on src.app.adapters and other domains, except the shared ones
```

```
src.app.di - IoC container and lifespan management
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

# Deploy k8s

## Deploy minikube

### Build container
```
docker build . -t backend:latest
```

### Create values.dev.yaml
Create `values.dev.yaml` in `.k8s/app`, use the example `values.dev.example.yaml`


### Set secrets or/and configmaps
Secret template:

```
apiVersion: v1
kind: Secret
metadata:
  name: <secret-name>
type: Opaque
stringData:
  KEY: VALUE (not base64)
```

ConfigMap template:
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: <configmap-name>
data:
  KEY: VALUE (not base64)
```

### Deploy
```
helm upgrade backend .k8s/app --install -f .k8s/app/values.yaml -f .k8s/app/values.dev.yaml
```