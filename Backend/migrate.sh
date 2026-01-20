#! /usr/bin/env bash


. ./venv/bin/activate
set -xe
python FinTrust/services/auth/auth_migrations.py 
python FinTrust/services/accounts/accounts_migrations.py
python FinTrust/services/transfers/transfers_migrations.py
