#!/bin/bash
SRCPATH=$(pwd)

if [ -d ".venv" ]
then
    . .venv/bin/activate
    pip install -r requirements.txt
    deactivate
fi
