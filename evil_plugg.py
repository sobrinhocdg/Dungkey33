import os
import sys
import time
import hashlib
import secrets
import random

sys.dont_write_bytecode = True

# Paleta Evil Plugg x Gnostic
C_PURP = "\033[38;5;93m"
C_MAGENTA = "\033[38;5;129m"
C_BLACK = "\033[1;30m"
C_RED = "\033[38;5;196m"
C_WHT = "\033[1;37m"
C_RST = "\033[0m"

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def glitch_text(text):
    """ Adiciona um efeito de estática visual do Evil Plugg """
    glitch_chars = ["!", "#", "$", "%", "&", "x", "†", "☥", "☠"]
    result = ""
    for char in text:
        if random.random() < 0.05 and char != " ":
            result += f"{C_RED}{random.choice(glitch_chars)}{C_PURP}"
        else:
            result += char
    return result

def manifestacao_reaper():
    limpar_tela()
    print(f"{C_PURP}")
    print("      ▄▄▄ . ▌ ▐·▪  ▄▄▌   ▄▄▄·▄▄▌  ▄• ▄▌ ▄▄ •  ▄▄ • ")
    print("      ▀▄.▀·▪█·█▌██ ██•  ▐█ ▄███•  █▪██▌▐█ ▀ ▪▐█ ▀ ▪")
    print("      ▐▀▀▪▄▐█▪█▌▐█·██▪   ██▀·██▪  █▌▐█▌▄█ ▀█▄▄█ ▀█▄")
    print("      ▐█▄▄▌ ███ ▐█▌▐█▌▐▌▐█▪·•▐█▌▐▌▐█▄█▌▐█▄▪▐█▐█▄▪▐█")
    print("       ▀▀▀ . ▀  ▀▀▀.▀▀▀ .▀   .▀▀▀  ▀▀▀ ·▀▀▀▀ ·▀▀▀▀ {C_RST}")
    print(f"{C_BLACK} [ EVIL PLUGG PROTOCOL - FORENSIC DATA OBLITERATOR ]{C_RST}")
    print(f"{C_MAGENTA}" + glitch_text("="*60) + f"{C_RST}\n")

def gerar_ruido_abissal(tamanho):
    """ Gera pura entropia criptográfica para corromper a matéria """
    return secrets.token_bytes(tamanho)

def ceifar_artefato(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"{C_RED}[!] O ALVO NÃO EXISTE NO PLANO MATERIAL.{C_RST}")
        return False

    tamanho_total = os.path.getsize(caminho_arquivo)
    chunk_size = 1024 * 1024  # Destrói 1 Megabyte por ciclo (Eficiência Sênior)
    
    print(f"{C_WHT}[+] ALVO ADQUIRIDO:{C_RST} {caminho_arquivo}")
    print(f"{C_WHT}[+] GRAVIDADE MATERIAL:{C_RST} {tamanho_total} bytes\n")
    
    try:
        with open(caminho_arquivo, "r+b") as f:
            # PASSE 1: O VAZIO (0x00)
            sys.stdout.write(f"{C_BLACK}[*] PASSE 1/3: INJETANDO O VAZIO ABSOLUTO... {C_RST}")
            sys.stdout.flush()
            for _ in range(0, tamanho_total, chunk_size):
                f.write(b'\x00' * chunk_size)
            f.flush()
            os.fsync(f.fileno())
            print(f"{C_MAGENTA}CONCLUÍDO{C_RST}")
            time.sleep(0.3)

            # PASSE 2: A LUZ DO PLEROMA (0xFF)
            f.seek(0)
            sys.stdout.write(f"{C_PURP}[*] PASSE 2/3: QUEIMANDO COM LUZ PLERÔMICA... {C_RST}")
            sys.stdout.flush()
            for _ in range(0, tamanho_total, chunk_size):
                f.write(b'\xff' * chunk_size)
            f.flush()
            os.fsync(f.fileno())
            print(f"{C_MAGENTA}CONCLUÍDO{C_RST}")
            time.sleep(0.3)

            # PASSE 3: EVIL PLUGG (Ruído Criptográfico)
            f.seek(0)
            sys.stdout.write(f"{C_RED}[*] PASSE 3/3: COLAPSO DE ENTROPIA (EVIL PLUGG)... {C_RST}")
            sys.stdout.flush()
            for _ in range(0, tamanho_total, chunk_size):
                ruido = gerar_ruido_abissal(chunk_size)
                f.write(ruido)
            f.flush()
            os.fsync(f.fileno())
            print(f"{C_MAGENTA}CONCLUÍDO{C_RST}")
            time.sleep(0.3)

        # PASSE 4: BANIMENTO FORENSE (Corrompe o nome do arquivo na tabela do HD)
        diretorio = os.path.dirname(caminho_arquivo)
        novo_nome = hashlib.sha3_256(str(time.time()).encode()).hexdigest() + ".void"
        caminho_corrompido = os.path.join(diretorio, novo_nome)
        
        os.rename(caminho_arquivo, caminho_corrompido)
        print(f"\n{C_WHT}[+] METADADOS DESTRUÍDOS. NOVO IDENTIFICADOR: {C_BLACK}{novo_nome[:15]}...{C_RST}")
        
        # PASSE 5: A FOICE (Delete final)
        os.remove(caminho_corrompido)
        print(f"{C_RED}[+] RASTROS APAGADOS. O ARQUIVO VOLTOU AO KENOMA.{C_RST}")

    except Exception as e:
        print(f"\n{C_RED}[!] FALHA NO RITUAL DE CEIFA: {e}{C_RST}")

def spawn_demiurge_artifact():
    """ Cria um arquivo de teste para você brincar de Deus sem quebrar seu PC """
    nome = "ilusao_material.txt"
    with open(nome, "w", encoding="utf-8") as f:
        f.write("DADOS SECRETOS DO KENOMA\n" * 10000) # Cria um arquivo gordinho
    return nome

if __name__ == "__main__":
    manifestacao_reaper()
    print(f"{C_BLACK}Aviso: O que for ceifado aqui não poderá ser recuperado por meios humanos.{C_RST}")
    
    # Prepara a cobaia
    alvo_teste = spawn_demiurge_artifact()
    
    alvo = input(f"\n{C_WHT}[?] ARRASTE O ARQUIVO PARA A FOICE (Ou aperte Enter para usar o arquivo de teste): {C_RST}").strip()
    
    # Remove aspas caso o usuário arraste o arquivo pro terminal
    alvo = alvo.strip('"').strip("'") 
    
    if not alvo:
        alvo = alvo_teste
        print(f"{C_BLACK}[*] Usando cobaia gerada ({alvo})...{C_RST}\n")
    
    ceifar_artefato(alvo)
    