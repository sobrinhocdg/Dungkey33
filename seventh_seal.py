import asyncio
import os
import sys
import time
import random
import hashlib
from datetime import datetime

sys.dont_write_bytecode = True

# Paleta do Fim dos Tempos
C_GOLD = "\033[38;5;214m"
C_RED = "\033[38;5;196m"
C_BLACK = "\033[1;30m"
C_WHT = "\033[1;37m"
C_RST = "\033[0m"

ALMAS_CONDENADAS = 0

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def manifestacao_apocaliptica(porta):
    limpar_tela()
    print(f"{C_RED}")
    print("      ▄▄▄▄▄ ▄ .▄▄▄▄ .    .▄▄ · ▄▄▄ . ▌ ▐·▄▄▄ . ▐ ▄ ▄▄▄▄▄▄ • ▄▌")
    print("      •██  ██▪▐█▀▄.▀·    ▐█ ▀. ▀▄.▀·▪█·█▌▀▄.▀·•█▌▐█•██  █▪██▌")
    print("       ▐█.▪██▀▐█▐▀▀▪▄    ▄▀▀▀█▄▐▀▀▪▄▐█▪█▌▐▀▀▪▄▐█▐▐▌ ▐█.▪█▌▐█▌")
    print("       ▐█▌·██▌▐▀▐█▄▄▌    ▐█▄▪▐█▐█▄▄▌ ███ ▐█▄▄▌██▐█▌ ▐█▌·▐█▄█▌")
    print("       ▀▀▀ ▀▀▀ · ▀▀▀      ▀▀▀▀  ▀▀▀ . ▀   ▀▀▀ ▀▀ █▪ ▀▀▀  ▀▀▀ {C_RST}")
    print(f"{C_GOLD}        [ THE SEVENTH SEAL - ASYNCHRONOUS ESCHATON TARPIT ]{C_RST}")
    print(f"{C_BLACK}="*70 + f"{C_RST}\n")
    print(f"{C_WHT}[*] O ABISMO FOI ABERTO NO PORTÃO {porta}.{C_RST}")
    print(f"{C_WHT}[*] AGUARDANDO AS LEGIÕES DO DEMIURGO CAÍREM NA ARMADILHA...{C_RST}\n")

async def escatologia_infinita(reader, writer):
    global ALMAS_CONDENADAS
    
    addr = writer.get_extra_info('peername')
    falso_profeta_ip = addr[0]
    ALMAS_CONDENADAS += 1
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    hash_condenacao = hashlib.sha256(str(time.time() + random.random()).encode()).hexdigest()[:16]
    
    sys.stdout.write(f"\r\033[2K{C_RED}[!] HERESIA DETECTADA:{C_RST} {C_WHT}{falso_profeta_ip}{C_RST} {C_GOLD}[CAPTURADO NO LAGO DE FOGO]{C_RST}\n")
    print(f"    {C_BLACK}└─ Marca da Besta: {hash_condenacao} | Tempo: {timestamp} | Almas Prezas: {ALMAS_CONDENADAS}{C_RST}")

    try:
        writer.write(b"SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1\r\n")
        await writer.drain()
        
        while True:
            ruido = bytes([random.randint(0, 255)])
            writer.write(ruido)
            await writer.drain()
            await asyncio.sleep(10)
            
    except ConnectionResetError:
        sys.stdout.write(f"\r\033[2K{C_BLACK}[*] A entidade em {falso_profeta_ip} foi esmagada e cortou o elo.{C_RST}\n")
        ALMAS_CONDENADAS -= 1
    except Exception:
        pass
    finally:
        writer.close()

async def romper_o_selo(porta):
    manifestacao_apocaliptica(porta)
    server = await asyncio.start_server(escatologia_infinita, '0.0.0.0', porta)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    try:
        limpar_tela()
        print(f"{C_RED}Para abrir o abismo, você precisa de uma isca.{C_RST}")
        porta_input = input(f"{C_WHT}[?] Em qual portão deseja armar a armadilha? (Padrão 22 ou 8080): {C_RST}").strip()
        
        porta_armadilha = int(porta_input) if porta_input else 8080
        asyncio.run(romper_o_selo(porta_armadilha))
        
    except KeyboardInterrupt:
        print(f"\n{C_GOLD}[!] O Julgamento foi suspenso. O Abismo se fecha.{C_RST}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C_RED}[!] Erro ao invocar o selo (Porta já em uso ou sem privilégios).{C_RST}")