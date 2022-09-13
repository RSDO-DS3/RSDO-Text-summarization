#!/bin/bash

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -r|--root-path) root_path="$2" ;;
    esac
    shift
done

eval "$(conda shell.bash hook)"
export ROOT="$root_path"
echo "Root folder set to $ROOT"

# metamodel
cd "$ROOT"/src/metamodel
conda create -n metamodel-local python=3.8
conda activate metamodel-local
pip3 install -r requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html
uvicorn main-fastapi:app --host 0.0.0.0 --port 5003 &

# graph-based
cd "$ROOT"/src/graph-based
conda create -n graph-based-local python=3.8
conda activate graph-based-local
pip3 install -r requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html
uvicorn main-fastapi:app --host 0.0.0.0 --port 5004 &

# t5-headline
cd "$ROOT"/src/t5-headline
conda create -n t5-headline-local python=3.8
conda activate t5-headline-local
pip3 install -r requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html
uvicorn main-fastapi:app --host 0.0.0.0 --port 5005 &

# t5-article
cd "$ROOT"/src/t5-article
conda create -n t5-article-local python=3.8
conda activate t5-article-local
pip3 install -r requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html
uvicorn main-fastapi:app --host 0.0.0.0 --port 5006 &

# sumbasic
cd "$ROOT"/src/sumbasic
conda create -n sumbasic-local python=3.8
conda activate sumbasic-local
pip3 install -r requirements.txt
uvicorn main-fastapi:app --host 0.0.0.0 --port 5007 &

# hybrid long
cd "$ROOT"/src/hybrid-long
conda create -n hybrid-long-local python=3.8
conda activate hybrid-long-local
pip3 install -r requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html
uvicorn main-fastapi:app --host 0.0.0.0 --port 5008 &
