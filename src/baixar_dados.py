from pathlib import Path

import requests

URL_BASE = "https://github.com/adaoduque/Brasileirao_Dataset/raw/refs/heads/master/"

ARQUIVOS = [
    "campeonato-brasileiro-full.csv",
    "campeonato-brasileiro-estatisticas-full.csv",
    "campeonato-brasileiro-gols.csv",
    "campeonato-brasileiro-cartoes.csv",
]

PASTA_RAW = Path("data/raw")


def baixar_arquivo(nome):
    url = URL_BASE + nome
    resposta = requests.get(url, timeout=30)
    resposta.raise_for_status()
    destino = PASTA_RAW / nome
    destino.write_bytes(resposta.content)
    print(f"Baixado: {destino} ({len(resposta.content) / 1024:.0f} KB)")


def main():
    PASTA_RAW.mkdir(parents=True, exist_ok=True)
    for nome in ARQUIVOS:
        baixar_arquivo(nome)


if __name__ == "__main__":
    main()