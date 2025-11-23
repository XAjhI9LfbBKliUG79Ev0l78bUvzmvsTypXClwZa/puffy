## About

- Jinja + htmx (https://picocss.com/docs) - styles
- FastAPI


## Build

**Podman/Docker**

```sh
podman build -t puffybuild .
```

```sh
podman run --rm -v "$(pwd):/app:z" puffybuild ./build.sh
```

## Run

TODO add params to run.sh
```sh
podman run --rm puffybuild ./run.sh
```
