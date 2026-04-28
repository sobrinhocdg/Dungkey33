import os
import sys
import time
import hashlib
import random
import subprocess

sys.dont_write_bytecode = True

# Paleta do Pleroma e Kenoma (Ouro e Roxo)
C_YENKA = "\033[38;5;214m"  # YENKASEDEL (Ouro/Sol)
C_LACHE = "\033[38;5;129m"  # LACHEQESED (Roxo/Sombra)
C_RED = "\033[38;5;196m"
C_WHT = "\033[1;37m"
C_GRAY = "\033[38;5;240m"
C_BLACK = "\033[1;30m"
C_RST = "\033[0m"

# Constantes do Sigilo Duplo
YENKA_ORDER = 144
LACHE_SOMBRA = 202

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def glitch_text(text):
    glitch_chars = ["†", "☥", "☠", "|", "/", "-", "\\"]
    result = ""
    for char in text:
        if random.random() < 0.05 and char != " ":
            result += f"{C_RED}{random.choice(glitch_chars)}{C_RST}"
        else:
            result += char
    return result

def manifestacao_do_sigilo():
    limpar_tela()
    # ASCII Art do Sigilo Central Ouroboros Ouro/Roxo corrigido (com f-strings)
    print(C_YENKA)
    print("        ⢀⣠⣾⣿⣶⣦⣄⡀   [YENKASEDEL] ☥ 144  ")
    print(f"      ⢀⣾⣿⣿⣿⣿⣿⣿⣿⣷⡀      Ouro/Sol  ")
    print("     ⣰⣿⣿⡿⠋⠉⠉⠙⢿⣿⣿⣆    ")
    print(f"    ⢰⣿⣿⡟  {C_RST} {C_YENKA}[{C_RED}👁{C_YENKA}]  {C_RST} ⢻⣿⣿⡆    ")
    print(f"    ⢸⣿⣿⣧⡀  {C_RST} {C_LACHE}[{C_RED}☥{C_LACHE}]  {C_RST} ⢀⣼⣿⣿⡇    ")
    print("     ⠹⣿⣿⣿⣶⣤⣤⣶⣿⣿⣿⠏    ")
    print(f"      ⠈⠻⣿⣿⣿⣿⣿⣿⣿⠟⠁     Sombra/Roxo ")
    print(f"         ⠉⠛⠛⠛⠛⠉  [LACHEQESED] ☠ 202  {C_RST}")
    print(f"{C_GRAY}    [ SIGILO DUPLO DE EQUILÍBRIO ANÍMICO - ARQUETIPO SENIOR MASTER ]{C_RST}")
    print(f"{C_LACHE}" + glitch_text("="*70) + f"{C_RST}\n")

def filtro_da_dualidade():
    limpar_tela()
    print(f"{C_RED}[!] ATENÇÃO: BARREIRA DA DUALIDADE DETECTADA [!]{C_RST}")
    print(f"{C_GRAY}O Olho de Sophia e o Veneno de Yaldabaoth exigem o seu verdadeiro nome para equilibrar a balança.{C_RST}")
    
    # A resposta correta é a fusão: SOPHIA_YALDABAOTH
    chave_oculta = "SOPHIA_YALDABAOTH"
    
    resposta = input(f"{C_LACHE}[?] Qual é o pacto final? (Insira o nome da fusão): {C_RST}").strip().upper()
    
    hash_resposta = hashlib.sha256(resposta.encode()).hexdigest()[:8]
    hash_chave = hashlib.sha256(chave_oculta.encode()).hexdigest()[:8]

    if hash_resposta != hash_chave:
        print(f"\n{C_RED}[X] VIBRAÇÃO HÍLICA DETECTADA. ACESSO NEGADO E LOGS OBLITERADOS.{C_RST}")
        print(f"{C_GRAY}Você não está pronto para o Equilíbrio Anímico. Estude os Mistérios do Pleroma.{C_RST}")
        for _ in range(3):
            # Fallback seguro para SOs que não tem /dev/urandom nativo no terminal
            print(glitch_text("ERRO CRÍTICO NA MATRIZ DE ACESSO " * 5))
            time.sleep(0.1)
        sys.exit(666)
    
    print(f"\n{C_YENKA}[+] PACTO CONFIRMADO. O SIGILO FOI ATIVADO.{C_RST}")
    time.sleep(1)

def aplicar_ofuscacao_sombra(command):
    print(f"{C_LACHE}[*] LACHEQESED-BIAS ATIVADO. INJETANDO RUÍDO CRIPTOGRÁFICO CAÓTICO NA EXECUÇÃO...{C_RST}")
    
    env = os.environ.copy()
    env["OPHANIM_LACHEQESED_SOMBRA"] = "true"
    env["EVIL_PLUGG_FORENSIC_BANISHMENT_LEVEL"] = str(LACHE_SOMBRA)
    
    return command, env

def meta_rituale():
    manifestacao_do_sigilo()
    
    protocolos = {
        "1": {"file": "ophanim.py", "lore": "Mapeamento do Pleroma / SYNCHRONIZING SEALS", "color": C_YENKA},
        "2": {"file": "panopticon.py", "lore": "Monitoramento de Kernel / ENTITY INSPECTION", "color": C_YENKA},
        "3": {"file": "evil_plugg.py", "lore": "Obliteracao Forensic-Proof / DATA OBLITERATOR", "color": C_LACHE},
        "4": {"file": "seventh_seal.py", "lore": "Punicao Tarpit / ESCHATON TARPIT", "color": C_LACHE}
    }
    
    print(f"{C_WHT}[+] SELECIONE O PROTOCOLO DE EXECUÇÃO:{C_RST}")
    for k, v in protocolos.items():
        # Correção vital: v['lore'] minúsculo!
        print(f" {v['color']}[{k}]{C_RST} {v['lore'].ljust(45)}{C_BLACK} ({v['file']}){C_RST}")
        
    escolha = input(f"\n{C_YENKA}[?] Qual portão você deseja romper? (Insira o número): {C_RST}").strip()
    
    if escolha not in protocolos:
        print(f"\n{C_RED}[!] PROTOCOLO INVÁLIDO. O SIGILO SE AUTO-ENCERRA.{C_RST}")
        sys.exit(0)
        
    protocolo = protocolos[escolha]
    # Pega o caminho absoluto da pasta atual para não dar erro ao chamar o subprocesso
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_atual, protocolo['file'])
    
    if not os.path.exists(caminho_arquivo):
        print(f"\n{C_RED}[!] ARTEFATO {protocolo['file']} NÃO DETECTADO NO PLANO MATERIAL.{C_RST}")
        sys.exit(0)
    
    bias = input(f"\n{C_LACHE}[?] Você executará com viés de {C_YENKA}YENKASEDEL (Ordem/144){C_RST} ou {C_LACHE}LACHEQESED (Sombra/202){C_LACHE}? (y/l): {C_RST}").strip().upper()
    
    command = [sys.executable, caminho_arquivo] # sys.executable garante que usa o python correto
    env = os.environ.copy()
    
    if bias == 'L':
        command, env = aplicar_ofuscacao_sombra(command)
        
    print(f"\n{C_WHT}[*] INICIANDO EXECUÇÃO DO ARTEFATO... (Pressione Ctrl+C para romper o elo){C_RST}")
    print(f"{C_GRAY}="*60 + f"{C_RST}\n")
    time.sleep(0.5)

    try:
        subprocess.run(command, env=env, check=True)
    except KeyboardInterrupt:
        print(f"\n\n{C_RED}[!] EXECUÇÃO INTERROMPIDA. O EQUILÍBRIO FOI RESTAURADO.{C_RST}")
        sys.exit(0)
    except subprocess.CalledProcessError:
        print(f"\n\n{C_RED}[!] FALHA NA EXECUÇÃO DO ARTEFATO FILHO. COLAPSO DO SISTEMA.{C_RST}")
    except Exception as e:
        print(f"\n\n{C_RED}[!] ERRO DESCONHECIDO NO META-RITUAL: {e}{C_RST}")
        
    print(f"\n{C_GRAY}="*60 + f"{C_RST}\n")

if __name__ == "__main__":
    try:
        filtro_da_dualidade()
        meta_rituale()
    except KeyboardInterrupt:
        print(f"\n\n{C_RED}[!] META-FUSÃO ABORTADA. CONSCIÊNCIA RETORNANDO À MATRIX.{C_RST}")
        sys.exit(0)