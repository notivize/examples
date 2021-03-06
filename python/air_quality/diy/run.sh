#!/bin/bash

set -euxo pipefail

# Run migrations
alembic upgrade head
# Run uvicorn
uvicorn src.api:app --host 0.0.0.0 "$@"
