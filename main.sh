#!/bin/bash

eval "$(conda shell.bash hook)"
export ROOT="/mnt/e/repositories/RSDO-DS3/"

# metamodel
conda activate metamodel-local
cd "$ROOT"/src/metamodel
uvicorn main-fastapi:app --host 0.0.0.0 --port 8000 &

# graph-based
conda activate graph-based-local
cd "$ROOT"/src/graph-based
uvicorn main-fastapi:app --host 0.0.0.0 --port 8001 &

# t5-headline
conda activate t5-local
cd "$ROOT"/src/t5-headline
uvicorn main-fastapi:app --host 0.0.0.0 --port 8002 &

# t5-article
conda activate t5-local
cd "$ROOT"/src/t5-article
uvicorn main-fastapi:app --host 0.0.0.0 --port 8003 &

# sumbasic
conda activate t5-local
cd "$ROOT"/src/sumbasic
uvicorn main-fastapi:app --host 0.0.0.0 --port 8004 &

# hybrid long
conda activate t5-local
cd "$ROOT"/src/hybrid-long
uvicorn main-fastapi:app --host 0.0.0.0 --port 8005 &




