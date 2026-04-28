import asyncio
import os
import sys
import time
import math

sys.dont_write_bytecode = True

# --- [ GEOMETRIA SAGRADA SÊNIOR ] ---
# C = sqrt(2^20) = 1024 conexões assíncronas
Concurrence_Limit = int(math.sqrt(1 << 20)) 
Raziel_Timeout = math.cos(math.pi / 3)  # 0.5 segundos

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
    print("\033[1;30m[ OPHANIM PROTOCOL V2 - ASTRAL PLANE SYNC ]\033[0m\n")

async def extrair_alma(reader, writer):
    """ Tenta arrancar a identidade (Banner) do serviço rodando na porta """
    try:
        # Envia um pulso para provocar uma resposta do servidor
        writer.write(b"HEAD / HTTP/1.0\r\n\r\n")
        await writer.drain()
        
        # Aguarda a resposta (a alma do serviço)
        data = await asyncio.wait_for(reader.read(100), timeout=0.5)
        alma = data.decode('utf-8', errors='ignore').split('\n')[0].strip()
        return alma if alma else "SILÊNCIO ABSOLUTO"
    except:
        return "ENTIDADE DESCONHECIDA"
    finally:
        writer.close()
        await writer.wait_closed()

async def julgamento_de_gabriel(Babel_Chord, gate, Metatron_Gate):
    """ Coroutine que julga a porta assincronamente """
    async with Metatron_Gate:
        try:
            # Abre conexão não-bloqueante (Magia Sênior)
            fut = asyncio.open_connection(Babel_Chord, gate)
            reader, writer = await asyncio.wait_for(fut, timeout=Raziel_Timeout)
            
            # Se conectou, a porta está aberta. Vamos extrair a alma.
            alma = await extrair_alma(reader, writer)
            
            # Exibe imediatamente o achado na tela
            print(f"\033[1;36m[Δ] SELO ROMPIDO: {gate} \033[1;30m--> {alma}\033[0m")
            Opened_Seals.append((gate, alma))
        except:
            pass # Porta fechada ou protegida

async def ritual_assincrono(Babel_Chord, Enochian_Limit):
    ressonancia_esoterica()
    print(f"\033[1;37m[+] Focando prisma no IP: {Babel_Chord}\033[0m")
    print(f"\033[1;37m[+] Invocando {Concurrence_Limit} coroutines para {Enochian_Limit} portões...\033[0m\n")
    
    start_time = time.time()

    # O Portão de Metatron controla para não sobrecarregar a rede local
    Metatron_Gate = asyncio.Semaphore(Concurrence_Limit)
    
    # Cria a matriz de tarefas (Tasks)
    tasks = [
        julgamento_de_gabriel(Babel_Chord, gate, Metatron_Gate) 
        for gate in range(1, Enochian_Limit + 1)
    ]
    
    # Executa todas as tarefas simultaneamente no plano astral
    await asyncio.gather(*tasks)

    end_time = time.time()
    
    print("\n\033[1;35m" + "∇"*50 + "\033[0m")
    print(f"\033[1;37m[!] Ritual convergido em {round(end_time - start_time, 2)} ciclos.\033[0m")
    print(f"\033[1;36m[+] Total de selos expostos: {len(Opened_Seals)}\033[0m")
    print("\033[1;35m" + "Δ"*50 + "\033[0m\n")

if __name__ == "__main__":
    # Garante compatibilidade do event loop em diferentes SOs
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    try:
        ressonancia_esoterica()
        alvo = input("\033[1;30m[?] Insira a coordenada mortal (IP alvo): \033[0m")
        alvo = alvo if alvo else "127.0.0.1"
        
        # Matemática de bits: 1 << 14 = 16384 portas 
        # (Agora que é assíncrono, podemos varrer milhares de portas em segundos)
        Limite = 1 << 14 
        
        # Dispara o event loop (núcleo do asyncio)
        asyncio.run(ritual_assincrono(alvo, Limite))
        
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Desconexão neural forçada. Abortando matriz.\033[0m")
        sys.exit(1)