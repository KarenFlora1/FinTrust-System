python FinTrust/services/auth/auth_server.py >> logs/auth.log &
python FinTrust/services/accounts/accounts_server.py >> logs/accounts.log &
python FinTrust/services/transfers/transfers_server.py >> logs/transfers.log &


python FinTrust/gateway/gateway.py | tee -a logs/gateway.log  @REM this will prin here and block