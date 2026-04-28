import asyncio
import os
import sys
import time
import math
import random
import hashlib

sys.dont_write_bytecode = True

# --- [ DOGMA GNÓSTICO - PARÂMETROS ASTRAIS ] ---
PLEROMA_CONCURRENCY = int(math.sqrt(1 << 20))  # 1024 Coroutines
ARCHON_TIMEOUT = math.cos(math.pi / 3)         # 0.5s Timeout

Opened_Seals = []

# Cores ANSI
C_PURPLE = "\033[38;5;93m"
C_CYAN = "\033[38;5;51m"
C_RED = "\033[38;5;196m"
C_GRAY = "\033[38;5;240m"
C_WHITE = "\033[1;37m"
C_RESET = "\033[0m"

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

async def typewriter(texto, atraso=0.01):
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        await asyncio.sleep(atraso)
    print()

async def neural_boot():
    """ Simula a conexão com o Pleroma (Interface Experimental) """
    limpar_tela()
    sys.stdout.write(C_GRAY)
    for i in range(5):
        mem_hex = f"0x{random.randint(100000, 999999):X}"
        await typewriter(f"[*] ALOCANDO MEMÓRIA GNÓSTICA ... {mem_hex} ... [OK]", 0.005)
    
    await typewriter("[*] DESVIANDO DO FIREWALL DEMIÚRGICO ... [BYPASS CONCLUÍDO]", 0.01)
    await typewriter("[*] SINTONIZANDO VIBRAÇÃO DOS ARCONTES ... \n", 0.02)
    sys.stdout.write(C_RESET)
    await asyncio.sleep(0.3)

def ressonancia_esoterica():
    print(C_PURPLE)
    print("      ⢀⣠⣾⣿⣶⣦⣄⡀      ")
    print("    ⢀⣾⣿⣿⣿⣿⣿⣿⣿⣷⡀    ")
    print("   ⣰⣿⣿⡿⠋⠉⠉⠙⢿⣿⣿⣆   ")
    print(f"  ⢰⣿⣿⡟   {C_CYAN}[☥]{C_PURPLE}   ⢻⣿⣿⡆  ")
    print("  ⢸⣿⣿⣧⡀      ⢀⣼⣿⣿⡇  ")
    print("   ⠹⣿⣿⣿⣶⣤⣤⣶⣿⣿⣿⠏   ")
    print("    ⠈⠻⣿⣿⣿⣿⣿⣿⣿⠟⠁    ")
    print(f"       ⠉⠛⠛⠛⠛⠉       {C_RESET}")
    print(f"{C_GRAY}[ OPHANIM PROTOCOL V3 - ANTI-DEMIURGE ARCHITECTURE ]{C_RESET}\n")

async def extrair_alma(reader, writer):
    try:
        writer.write(b"HEAD / HTTP/1.0\r\n\r\n")
        await writer.drain()
        data = await asyncio.wait_for(reader.read(100), timeout=0.5)
        alma = data.decode('utf-8', errors='ignore').split('\n')[0].strip()
        return alma if alma else "SILÊNCIO DO ABISMO"
    except:
        return "ENTIDADE DESCONHECIDA"
    finally:
        writer.close()
        await writer.wait_closed()

async def interrogatorio_arconte(Babel_Chord, gate, Metatron_Gate):
    async with Metatron_Gate:
        try:
            fut = asyncio.open_connection(Babel_Chord, gate)
            reader, writer = await asyncio.wait_for(fut, timeout=ARCHON_TIMEOUT)
            alma = await extrair_alma(reader, writer)
            
            # \033[2K limpa a linha atual, \r volta pro começo. Isso evita quebrar a UI animada.
            sys.stdout.write(f"\r\033[2K{C_CYAN}[Δ] ARCONTE EXPOSTO (PORTA {gate}): {C_WHITE}{alma}{C_RESET}\n")
            Opened_Seals.append(gate)
        except:
            pass

async def animacao_ritualistica(tasks_rodando):
    """ Uma thread paralela que cria um efeito visual de processamento no rodapé """
    simbolos = ["|", "/", "-", "\\"]
    i = 0
    while not tasks_rodando.done():
        sys.stdout.write(f"\r{C_GRAY}[{simbolos[i]}] Injetando no Pleroma... Mapeando matriz material...{C_RESET}")
        sys.stdout.flush()
        i = (i + 1) % len(simbolos)
        await asyncio.sleep(0.1)
    # Limpa a linha de carregamento quando terminar
    sys.stdout.write("\r\033[2K")

def gerar_assinatura(alvo, portas_encontradas, tempo_execucao):
    """ Gera um hash criptográfico real para validar o escaneamento """
    dado_bruto = f"{alvo}_{portas_encontradas}_{tempo_execucao}_OPHANIM"
    hash_sig = hashlib.sha256(dado_bruto.encode()).hexdigest()
    
    print(f"{C_PURPLE}="*60)
    print(f"{C_WHITE}[+] RITUAL CONVERGIDO EM {round(tempo_execucao, 3)} SEGUNDOS")
    print(f"{C_WHITE}[+] TOTAL DE ARCONTES EXPOSTOS: {len(portas_encontradas)}")
    print(f"\n{C_GRAY}--- BEGIN OPHANIM CRYPTOGRAPHIC SIGNATURE ---")
    print(f"Target: {alvo}")
    print(f"Seals: {portas_encontradas}")
    print(f"Hash: {hash_sig}")
    print(f"--- END OPHANIM CRYPTOGRAPHIC SIGNATURE ---{C_RESET}")
    print(f"{C_PURPLE}="*60 + f"{C_RESET}\n")

async def invocar_pleroma(Babel_Chord, Enochian_Limit):
    await neural_boot()
    ressonancia_esoterica()
    print(f"{C_WHITE}[*] Fixando âncora no IP: {Babel_Chord}{C_RESET}")
    print(f"{C_WHITE}[*] Invocando {PLEROMA_CONCURRENCY} vetores contra {Enochian_Limit} portões...\033[0m\n")
    
    start_time = time.time()
    Metatron_Gate = asyncio.Semaphore(PLEROMA_CONCURRENCY)
    
    # Prepara as rotinas de escaneamento
    escaneamentos = [
        interrogatorio_arconte(Babel_Chord, gate, Metatron_Gate) 
        for gate in range(1,