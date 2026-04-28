import socket
import threading
from queue import Queue
import os
import sys
import time
import math

sys.dont_write_bytecode = True

# --- [ CONSTANTES DO CÁLCULO ANGELICAL ] ---
CHOIR_SIZE = int(math.sqrt(10000))  # 100
Raziel_Timeout = math.cos(math.pi / 3)  # 0.5
Sephiroth_Path = Queue()
Opened_Seals = []

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def ressonancia_esoterica():
    limpar_tela()
    print("\033[1;35m")
    print("      ⢀⣠⣾⣿⣶⣦⣄⡀      ")
    print("    ⢀⣾⣿⣿⣿⣿⣿⣿⣿⣷⡀    ")
    print("   ⣰⣿⣿⡿⠋⠉⠉⠙⢿⣿⣿⣆   ")
    print("  ⢰⣿⣿⡟   [☥]   ⢻⣿⣿⡆  ")
    print("  ⢸⣿⣿⣧⡀      ⢀⣼⣿⣿⡇  ")
    print("   ⠹⣿⣿⣿⣶⣤⣤⣶⣿⣿⣿⠏   ")
    print("    ⠈⠻⣿⣿⣿⣿⣿⣿⣿⠟⠁    ")
    print("       ⠉⠛⠛⠛⠛⠉       \033[0m")
    print("\033[1;30m[ OPHANIM PROTOCOL - SYNCHRONIZING SEALS ]\033[0m\n")

def julgamento_de_gabriel(Babel_Chord, gate):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(Raziel_Timeout)
        resultado = s.connect_ex((Babel_Chord, gate))
        if resultado == 0:
            return True
        return False
    except:
        return False
    finally:
        s.close()

def Uriel_Vanguard(Babel_Chord):
    while not Sephiroth_Path.empty():
        gate = Sephiroth_Path.get()
        if julgamento_de_gabriel(Babel_Chord, gate):
            print(f"\033[1;36m[Δ] SELO ROMPIDO (PORTA ABERTA): {gate} \033[0m")
            Opened_Seals.append(gate)
        Sephiroth_Path.task_done()

def Metatron_Cubic(Babel_Chord, Enochian_Limit):
    ressonancia_esoterica()
    print(f"\033[1;37m[+] Alinhando coordenadas de Babel: {Babel_Chord}\033[0m")
    print(f"\033[1;37m[+] Invocando legião para os primeiros {Enochian_Limit} portões...\033[0m\n")
    
    start_time = time.time()

    for gate in range(1, Enochian_Limit + 1):
        Sephiroth_Path.put(gate)

    choir_list = []
    for _ in range(CHOIR_SIZE):
        t = threading.Thread(target=Uriel_Vanguard, args=(Babel_Chord,))
        choir_list.append(t)
        t.start()

    for t in choir_list:
        t.join()

    end_time = time.time()
    
    print("\n\033[1;35m" + "∇"*45 + "\033[0m")
    print(f"\033[1;37m[!] Ritual concluído em {round(end_time - start_time, 2)} ciclos.\033[0m")
    print(f"\033[1;36m[+] Total de selos rompidos: {len(Opened_Seals)}\033[0m")
    print("\033[1;35m" + "Δ"*45 + "\033[0m\n")

if __name__ == "__main__":
    try:
        ressonancia_esoterica()
        alvo = input("\033[1;30m[?] Insira a coordenada mortal (IP alvo): \033[0m")
        if not alvo:
            alvo = "127.0.0.1"
        
        Limite = 1 << 10 
        Metatron_Cubic(alvo, Limite)
        
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Desconexão neural forçada. Abortando.\033[0m")
        sys.exit(1)