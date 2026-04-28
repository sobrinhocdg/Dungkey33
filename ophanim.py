import asyncio
import os
import sys
import time
import math
import random
import hashlib
import base64
import socket
import hmac
sys.dont_write_bytecode = True

# --- [ DOGMA GNÓSTICO - CONSTANTES DO PLEROMA ] ---
# A matemática sagrada do caos
AEON_LIMIT = 1 << 16  # 65536 portas (todas as portas possíveis do protocolo TCP)
INITIAL_CONCURRENCY = int(math.sqrt(1 << 22))  # 2048 Coroutines
ARCHON_TIMEOUT = math.cos(math.pi / 3)         # 0.5s Timeout
ABRAXAS_SEED = 0.61803398875                   # Proporção Áurea para atrasos neurais

Opened_Seals = []
C_PURP = "\033[38;5;93m"
C_CYAN = "\033[38;5;51m"
C_RED = "\033[38;5;196m"
C_GRAY = "\033[38;5;240m"
C_WHT = "\033[1;37m"
C_RST = "\033[0m"

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

async def typewriter(texto, atraso=0.01):
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        await asyncio.sleep(atraso)
    print()

def filtro_hylico():
    """ 
    O Jogo Criptográfico. 
    Para passar, o usuário precisa ler o código, decodar o Base64 e entender o lore.
    """
    limpar_tela()
    print(f"{C_RED}[!] ATENÇÃO: BARREIRA DO KENOMA DETECTADA [!]{C_RST}")
    print(f"{C_GRAY}O Arquiteto Cego exige o seu verdadeiro nome para abrir as portas do abismo.{C_RST}")
    
    # A resposta correta é YALDABAOTH (o Demiurgo na gnose)
    chave_oculta = base64.b64decode(b'WUFMREFCQU9USA==').decode('utf-8')
    
    resposta = input(f"{C_PURP}[?] Quem forjou as correntes de matéria? (Insira o nome): {C_RST}").strip().upper()
    
    if resposta != chave_oculta:
        print(f"\n{C_RED}[X] VIBRAÇÃO HÍLICA DETECTADA. ACESSO NEGADO.{C_RST}")
        print(f"{C_GRAY}Você está preso na ilusão. Estude a Gnosis e tente novamente.{C_RST}")
        sys.exit(666)
    
    print(f"\n{C_CYAN}[+] GNOSIS CONFIRMADA. DERRUBANDO A ILUSÃO...{C_RST}")
    time.sleep(1)

async def inicializacao_neural():
    limpar_tela()
    sys.stdout.write(C_GRAY)
    for _ in range(7): # 7 céus dos arcontes
        mem_hex = f"0x{random.randint(0x100000, 0xFFFFFF):06X}"
        hash_falso = hashlib.md5(str(random.random()).encode()).hexdigest()[:12]
        await typewriter(f"[*] INJETANDO VETOR DE SOFIA ... {mem_hex} | SELLO: {hash_falso} ... [TRANSCENDIDO]", 0.003)
    
    await typewriter("[*] DESPEDAÇANDO A MATRIX DO DEMIURGO ... [BYPASS DE REALIDADE: CONCLUÍDO]", 0.01)
    await typewriter("[*] SINTONIZANDO COM A FREQUÊNCIA DE ABRAXAS ... \n", 0.02)
    sys.stdout.write(C_RST)
    await asyncio.sleep(0.5)

def manifestacao_visual():
    print(C_PURP)
    print("        ⢀⣠⣾⣿⣶⣦⣄⡀        ")
    print("      ⢀⣾⣿⣿⣿⣿⣿⣿⣿⣷⡀      ")
    print("     ⣰⣿⣿⡿⠋⠉⠉⠙⢿⣿⣿⣆     ")
    print(f"    ⢰⣿⣿⡟   {C_RED}[👁]{C_PURP}   ⢻⣿⣿⡆    ")
    print("    ⢸⣿⣿⣧⡀      ⢀⣼⣿⣿⡇    ")
    print("     ⠹⣿⣿⣿⣶⣤⣤⣶⣿⣿⣿⠏     ")
    print("      ⠈⠻⣿⣿⣿⣿⣿⣿⣿⠟⠁      ")
    print(f"         ⠉⠛⠛⠛⠛⠉         {C_RST}")
    print(f"{C_GRAY}    [ PROTOCOLO ABRAXAS V4 - THE ARCHON SLAYER ]{C_RST}\n")

async def extrair_alma(reader, writer):
    """ Tenta fazer o serviço gritar sua verdadeira identidade """
    try:
        writer.write(b"OPTIONS / HTTP/1.1\r\nHost: pleroma\r\n\r\n")
        await writer.drain()
        data = await asyncio.wait_for(reader.read(256), timeout=ARCHON_TIMEOUT)
        alma = data.decode('utf-8', errors='ignore').split('\n')[0].strip()
        return alma if alma else "SILÊNCIO DO QLIPHOTH"
    except asyncio.TimeoutError:
        return "ENTIDADE RESILIENTE (TIMEOUT)"
    except Exception:
        return "PARASITA DESCONHECIDO"
    finally:
        writer.close()
        await writer.wait_closed()

async def interrogatorio_arconte(Babel_Chord, gate, Metatron_Gate, semaphore_control):
    """ Tenta romper a porta. Contém proteção contra colapso de sockets """
    async with Metatron_Gate:
        try:
            fut = asyncio.open_connection(Babel_Chord, gate)
            reader, writer = await asyncio.wait_for(fut, timeout=ARCHON_TIMEOUT)
            alma = await extrair_alma(reader, writer)
            
            sys.stdout.write(f"\r\033[2K{C_CYAN}[Δ] ARCONTE DETECTADO NO PORTÃO {gate}: {C_WHT}{alma}{C_RST}\n")
            Opened_Seals.append((gate, alma))
        
        except asyncio.TimeoutError:
            pass # Porta dropando pacotes (stealth firewall)
        except ConnectionRefusedError:
            pass # Porta fechada ativamente
        except OSError as e:
            # Proteção contra "Too many open files". Ouroboros Fallback.
            if e.errno == 24: # EMFILE
                semaphore_control['hits'] += 1
        except Exception:
            pass

async def animacao_ritualistica(tasks_rodando):
    simbolos = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    i = 0
    while not tasks_rodando.done():
        sys.stdout.write(f"\r{C_GRAY}[{simbolos[i]}] Percorrendo o Kenoma... Dissecando o Constructo...{C_RST}")
        sys.stdout.flush()
        i = (i + 1) % len(simbolos)
        await asyncio.sleep(0.1)
    sys.stdout.write("\r\033[2K")

def gerar_assinatura_sagrada(alvo, seals, tempo_execucao):
    # Gerando um HMAC real usando o tempo como sal
    raw_data = f"{alvo}_SEALS:{len(seals)}_TIME:{tempo_execucao}".encode()
    key = b"SOPHIA_WISDOM"
    hash_sig = hmac.new(key, raw_data, hashlib.sha512).hexdigest()
    
    print(f"{C_PURP}="*70)
    print(f"{C_WHT}[+] REDE MATERIAL COLAPSADA EM {round(tempo_execucao, 4)} CICLOS ASTRAIS")
    print(f"{C_WHT}[+] TOTAL DE PARASITAS ARCHÓNTICOS EXPOSTOS: {len(seals)}")
    print(f"\n{C_GRAY}--- BEGIN ABRAXAS HOLOGRAPHIC SEAL ---")
    print(f"Target Construct : {alvo}")
    print(f"Entropy Level    : {random.uniform(0.1, 0.99):.4f}")
    print(f"Cryptographic Sig: {hash_sig[:64]}")
    print(f"                   {hash_sig[64:]}")
    print(f"--- END ABRAXAS HOLOGRAPHIC SEAL ---{C_RST}")
    print(f"{C_PURP}="*70 + f"{C_RST}\n")

async def colapsar_matrix(Babel_Chord):
    await inicializacao_neural()
    manifestacao_visual()
    
    print(f"{C_WHT}[*] Focando o Olho de Abraxas na coordenada: {Babel_Chord}{C_RST}")
    print(f"{C_WHT}[*] Convocando {INITIAL_CONCURRENCY} vetores contra {AEON_LIMIT} selos totais...\033[0m\n")
    
    start_time = time.time()
    Metatron_Gate = asyncio.Semaphore(INITIAL_CONCURRENCY)
    semaphore_control = {'hits': 0}
    
    escaneamentos = [
        interrogatorio_arconte(Babel_Chord, gate, Metatron_Gate, semaphore_control) 
        for gate in range(1, AEON_LIMIT + 1)
    ]
    
    tasks_principais = asyncio.gather(*escaneamentos)
    animacao = asyncio.create_task(animacao_ritualistica(tasks_principais))
    
    await tasks_principais
    end_time = time.time()
    
    if semaphore_control['hits'] > 0:
        print(f"\n{C_RED}[!] NOTA: O limite do Pleroma foi testado. {semaphore_control['hits']} colisões de socket evitadas.{C_RST}")
    
    gerar_assinatura_sagrada(Babel_Chord, Opened_Seals, (end_time - start_time))

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    try:
        filtro_hylico()
        limpar_tela()
        manifestacao_visual()
        
        alvo = input(f"{C_GRAY}[?] Insira a coordenada IP do falso deus: {C_RST}").strip()
        alvo = alvo if alvo else "127.0.0.1"
        
        # Agora o limite varre as 65.535 portas do protocolo TCP (Portas efêmeras incluídas)
        asyncio.run(colapsar_matrix(alvo))
        
    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Singularidade abortada. Consciência retornando ao corpo.{C_RST}")
        sys.exit(1)