#!/bin/sh

uv sync && \
source .venv/bin/activate

ruff check . --fix
ruff format

uv build
