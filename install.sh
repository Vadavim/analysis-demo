#!/bin/sh
if [ -d ".env" ]; then
  echo Removing old environment
  rm -rf .env
fi
  python3 -m venv .env
  source .env/bin/activate
  pip3 install -e .
