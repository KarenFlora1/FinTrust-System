import os

base_folder     =   os.path.dirname(__file__)
venv_py         =   os.path.join(base_folder, "venv", "bin", "python")
service_folder  =   os.path.join(base_folder,"FinTrust", "services")
gateway_folder  =   os.path.join(base_folder,"FinTrust", "gateway")
auth_folder     =   os.path.join(service_folder, "auth")
accounts_folder  =   os.path.join(service_folder, "accounts")
transfers_folder  =   os.path.join(service_folder, "transfers")
