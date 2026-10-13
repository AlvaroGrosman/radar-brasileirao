from pathlib import Path

import numpy as np
import pandas as pd

ARQUIVO_BRUTO = Path("data/raw/campeonato-brasileiro-full.csv")
PASTA_PROCESSADA = Path("data/processed")
ARQUIVO_LIMPO = PASTA_PROCESSADA / "partidas_limpas.csv"

PRIMEIRA_TEMPORADA = 2003
LIMITE_DIAS_ENTRE_TEMPORADAS = 60


def carregar_dados():
    return pd.read_csv(ARQUIVO_BRUTO)


def limpar_partidas(partidas):
    partidas = partidas.copy()

    # 1. Corrige o nome da coluna
    partidas = partidas.rename(columns={"rodata": "rodada"})

    # 2. Converte texto em data de verdade
    partidas["data"] = pd.to_datetime(partidas["data"], format="%d/%m/%Y")

    # 3. Cria a temporada: uma nova temporada começa quando a rodada "volta" para trás
    partidas = partidas.sort_values(["data", "ID"]).reset_index(drop=True)
    dias_desde_jogo_anterior = partidas["data"].diff().dt.days
    nova_temporada = dias_desde_jogo_anterior > LIMITE_DIAS_ENTRE_TEMPORADAS
    partidas["temporada"] = PRIMEIRA_TEMPORADA + nova_temporada.cumsum()

    # 4. Cria colunas derivadas
    partidas["total_gols"] = partidas["mandante_Placar"] + partidas["visitante_Placar"]

    condicoes = [
        partidas["mandante_Placar"] > partidas["visitante_Placar"],
        partidas["mandante_Placar"] < partidas["visitante_Placar"],
    ]
    escolhas = ["vitoria_mandante", "vitoria_visitante"]
    partidas["resultado"] = np.select(condicoes, escolhas, default="empate")

    return partidas


def validar(partidas):
    print("Jogos por temporada:")
    print(partidas["temporada"].value_counts().sort_index())
    print()

    diferentes = partidas[partidas["temporada"] != partidas["data"].dt.year]
    print("Jogos em que a temporada é diferente do ano da data:", len(diferentes))
    print(diferentes.groupby("temporada")["data"].agg(["min", "max", "count"]))
    print()

    # 'vencedor' é "-" quando há empate: tem que bater com a coluna que criamos
    inconsistentes = partidas[
        (partidas["resultado"] == "empate") != (partidas["vencedor"] == "-")
    ]
    print("Linhas em que 'resultado' e 'vencedor' discordam:", len(inconsistentes))
    print(
        inconsistentes[
            ["ID", "data", "mandante", "visitante", "mandante_Placar", "visitante_Placar", "vencedor", "resultado"]
        ]
    )


def main():
    partidas = carregar_dados()
    partidas_limpas = limpar_partidas(partidas)
    validar(partidas_limpas)

    PASTA_PROCESSADA.mkdir(parents=True, exist_ok=True)
    partidas_limpas.to_csv(ARQUIVO_LIMPO, index=False)
    print()
    print(f"Arquivo salvo em {ARQUIVO_LIMPO} com {len(partidas_limpas)} linhas")


if __name__ == "__main__":
    main()