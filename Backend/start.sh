#! /usr/bin/env sh

#This is poors microservice starter
#Gotta kill all process manually to restart good luck maintaing this scritp

#TODO: all this commands should be contralable by a configurable script
#TODO: monitor processes, restart them individually
#TODO: print pids in a more convinient way

. ./venv/bin/activate
set -xe

mkdir -p logs

python FinTrust/services/auth/auth_server.py >> logs/auth.log &
python FinTrust/services/accounts/accounts_server.py >> logs/accounts.log &
python FinTrust/services/transfers/transfers_server.py >> logs/transfers.log &


python FinTrust/gateway/gateway.py | tee -a logs/gateway.log  # this will prin here and block
