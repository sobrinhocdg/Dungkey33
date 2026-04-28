import os
import sys
import time
import hashlib
import psutil
from datetime import datetime

sys.dont_write_bytecode = True

# Paleta de Cores Opressora
C_RED = "\033[38;5;196m"
C_BLOOD = "\033[38;5;88m"
C_GOLD = "\033[38;5;214m"
C_GRAY = "\033[38;5;240m"
C_DIM = "\033[38;5;236m"
C_WHT = "\033[1;37m"
C_RST = "\033[0m"

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def renderizar_cabecalho():
    limpar_tela()
    print(f"{C_RED}")
    print(" ▄▄▄· ▄▄▄ . ▄▄▄· ▐ ▄       ▄▄▄·▄▄▄▄▄▪   ▄▄· ▄▄▄▄▄▄▄▌ ▐ ▄ ")
    print("▐█ ▄█▀▄.▀·▐█ ▀█ •█▌▐█▪     ▐█ ▄█•██  ██ ▐█ ▌▪•██  ██· █▌▐█")
    print(" ██▀·▐▀▀▪▄▄█▀▀█ ▐█▐▐▌ ▄█▀▄  ██▀· ▐█.▪▐█·██ ▄▄ ▐█.▪██▪▐█▐▐▌")
    print("▐█▪·•▐█▄▄▌▐█ ▪▐▌██▐█▌▐█▌.▐▌▐█▪·• ▐█▌·▐█▌▐███▌ ▐█▌·▐█▌██▐█▌")
    print(".▀    ▀▀▀  ▀  ▀ ▀▀ █▪ ▀█▄▀▪.▀    ▀▀▀ ▀▀▀·▀▀▀  ▀▀▀  ▀▀▀▀ █▪{C_RST}")
    print(f"{C_GOLD}   [ AEON PANOPTICON - OMNISCIENT KERNEL INTROSPECTION ]{C_RST}")
    print(f"{C_GRAY}="*65 + f"{C_RST}\n")

def buscar_entidades():
    entidades = []
    # Itera sobre todos os processos vivos no sistema
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            info = proc.info
            # Ignora processos mortos ou vazios
            if info['name'] and info['memory_percent']:
                entidades.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    # Ordena as entidades pelo peso material (Uso de RAM)
    entidades = sorted(entidades, key=lambda e: e['memory_percent'], reverse=True)
    return entidades[:15] # Pega apenas os 15 lordes mais pesados

def vigilia_eterna():
    try:
        while True:
            renderizar_cabecalho()
            lordes = buscar_entidades()
            
            # Estatísticas Globais do Pleroma
            cpu_global = psutil.cpu_percent()
            ram_global = psutil.virtual_memory().percent
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            print(f"{C_WHT}[+] RUPTURA DO VÉU: {timestamp}{C_RST}")
            print(f"{C_WHT}[+] ESTRESSE DA MATRIX (CPU): {C_RED if cpu_global > 80 else C_GOLD}{cpu_global}%{C_RST}")
            print(f"{C_WHT}[+] GRAVIDADE MATERIAL (RAM): {C_RED if ram_global > 80 else C_GOLD}{ram_global}%{C_RST}\n")
            
            # Cabeçalho da Tabela
            print(f"{C_BLOOD}   FATE_ID   | ENTITY_CLASS         | MATERIAL_WEIGHT | CPU_PULSE{C_RST}")
            print(f"{C_DIM}" + "-"*65 + f"{C_RST}")
            
            for ent in lordes:
                pid = str(ent['pid']).ljust(9)
                nome = str(ent['name'])[:20].ljust(20) # Trunca nomes grandes
                ram = f"{ent['memory_percent']:.2f}%".ljust(15)
                cpu = f"{ent['cpu_percent']:.1f}%"
                
                # Gera uma assinatura falsa pra cada processo para estética
                hash_falso = hashlib.md5(f"{pid}{nome}".encode()).hexdigest()[:6]
                
                print(f" {C_GRAY}[{hash_falso}]{C_RST} {C_WHT}{pid}{C_RST}| {C_GOLD}{nome}{C_RST} | {C_RED}{ram}{C_RST} | {C_WHT}{cpu}{C_RST}")
            
            print(f"\n{C_GRAY}[*] O Olho não pisca. Pressione Ctrl+C para cegá-lo.{C_RST}")
            
            # O ritual se repete a cada 1.5 segundos
            time.sleep(1.5)
            
    except KeyboardInterrupt:
        print(f"\n\n{C_RED}[!] VIGÍLIA ENCERRADA. OS ARCONTES VOLTAM ÀS SOMBRAS.{C_RST}")
        sys.exit(0)

if __name__ == "__main__":
    vigilia_eterna()