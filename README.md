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

First, ensure you have activated your virtual environment:
```sh
source .venv/bin/activate
```

Then, run the application using uvicorn:
```sh
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```
