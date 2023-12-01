#! /bin/bash

PRE='export $(cat '
POST='/.env.local | xargs)'
CMD=$PRE$1$POST
echo $CMD >> ~/.bashrc

apt update && apt install -y postgresql-client
poetry config virtualenvs.in-project true
poetry install
