import os
import subprocess
import platform

def build_service(cmds):
    print(f"[build] Executando: {' '.join(cmds)}")
    try:
        result = subprocess.run(cmds, capture_output=True, text=True, check=True, shell=True)
        print(result.stdout)
        if result.stderr:
            print("[stderr]", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"[build] ERRO ao executar {cmds[0]}:\n{e.stderr}")
        raise

IS_WINDOWS = platform.system() == "Windows"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICES = ["auth", "accounts", "transfers", "gateway"]

for svc in SERVICES:
    service_dir = os.path.join(ROOT_DIR, "services", svc)
    proto_file = os.path.join(service_dir, f"{svc}.proto")
    if os.path.exists(proto_file):
        print(f"\n=== Gerando Protos para {svc} ===")
        if IS_WINDOWS:
            build_cmd = [f'cmd', '/c', f'call scripts\\build_protos.cmd']
        else:
            build_cmd = ['bash', '-c', 'scripts/build_protos.sh']
        build_service(build_cmd)
    else:
        print(f"[info] Nenhum .proto encontrado para {svc}")

print("\n=== Migrando base de dados ===")
if IS_WINDOWS:
    migrate_cmd = ["cmd", "/c", "call scripts\\migrate.cmd"]
else:
    migrate_cmd = ["bash", "-c", "scripts/migrate.sh"]
build_service(migrate_cmd)

print("\n✅ Build concluído com sucesso.")
